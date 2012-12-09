/* safeexec (safe execution environment)
 *
 * From Mooshak versions 1.4 and 1.6
 * niceness by http://github.com/ochko/safeexec
 * this version by http://github.com/daveagp
 *
 * see README
 */

#define _BSD_SOURCE		/* to include wait4 function prototype */
#define _POSIX_SOURCE		/* to include kill  function prototype */

#include <sys/types.h>
#include <unistd.h>
#include <grp.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <sys/stat.h>
#include <ctype.h>
#include <sys/select.h>
#include <fcntl.h>
#include <assert.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <signal.h>
#include <sys/wait.h>
#include <time.h>
#include <stdarg.h>
#include <time.h>

#include "safe.h"

#define SIZE          8192	/* buffer size for reading /proc/<pid>/status */
#define INTERVAL        67	/* about 15 times a second                    */

#define INFINITY 0xFFFFFFFF

struct config
{
  rlim_t cpu;
  rlim_t memory;
  rlim_t core;
  rlim_t stack;
  rlim_t fsize;
  rlim_t nproc;
  rlim_t clock;

  rlim_t nfile;
  int niceness;

  gid_t gid;
  int uidplus;
  uid_t theuid;

  char *report_file;
  char *chroot_dir;
  char *exec_dir;
  char *env_vars;
};


struct config profile = { 10, 32768, 0, 8192, 0, 0, 60,
			  512, 16, 
			  1000, 10000, 0,
			  NULL, NULL, NULL, NULL };

struct config *pdefault = &profile;

pid_t pid;			/* is global, because we kill the proccess in alarm handler */
int mark;
int silent = 0;
FILE *redirect;

enum
  { OK, OLE, MLE, TLE, RTLE, RF, IE, RETNZ, TERM };	/* for the output statistics */
enum
  { EAT_INT, EAT_2INT, EAT_STRING, ERROR, EXECUTE, PARSE }; /* for the parsing */ 

char *names[] = {
  "UNKONWN",			/*  0 */
  "SIGHUP",			/*  1 */
  "SIGINT",			/*  2 */
  "SIGQUIT",			/*  3 */
  "SIGILL",			/*  4 */
  "SIGTRAP",			/*  5 */
  "SIGABRT",			/*  6 */
  "SIGBUS",			/*  7 */
  "SIGFPE",			/*  8 */
  "SIGKILL",			/*  9 */
  "SIGUSR1",			/* 10 */
  "SIGSEGV",			/* 11 */
  "SIGUSR2",			/* 12 */
  "SIGPIPE",			/* 13 */
  "SIGALRM",			/* 14 */
  "SIGTERM",			/* 15 */
  "SIGSTKFLT",			/* 16 */
  "SIGCHLD",			/* 17 */
  "SIGCONT",			/* 18 */
  "SIGSTOP",			/* 19 */
  "SIGTSTP",			/* 20 */
  "SIGTTIN",			/* 21 */
  "SIGTTOU",			/* 22 */
  "SIGURG",			/* 23 */
  "SIGXCPU",			/* 24 */
  "SIGXFSZ",			/* 25 */
  "SIGVTALRM",			/* 26 */
  "SIGPROF",			/* 27 */
  "SIGWINCH",			/* 28 */
  "SIGIO",			/* 29 */
  "SIGPWR",			/* 30 */
  "SIGSYS",			/* 31 */
};

void error (char *format, ...) {
  va_list p;
  if (format == NULL)
    error ("%s", strerror (errno));
  else {
    fprintf (stderr, "error %d (%s): ", errno, strerror(errno));
    va_start (p, format);
    vfprintf (stderr, format, p);
    va_end (p);
    fprintf (stderr, "\n");
  }
  exit (EXIT_FAILURE);
}

void printstats (const char *format, ...) { /* printf to the report file */ 
  va_list p;
  if (silent == 1)
    return;
  va_start (p, format);
  vfprintf (redirect, format, p);
  va_end (p);
}

char *name (int signal) {
  if (signal >= sizeof (names) / sizeof (char *))
    signal = 0;
  return (names[signal]);
}

int max (int a, int b) {
  return (a > b ? a : b);
}

void terminate (pid_t pid) {
  if (kill (pid, SIGKILL) < 0 && errno != ESRCH)
    error (NULL);
}

int milliseconds (struct timeval *tv)
{
  return ((int) tv->tv_sec * 1000 + (int) tv->tv_usec / 1000);
}

/* high resolution (microsecond) sleep */
void msleep (int ms) {
  struct timeval tv;
  int v;
  do
    {
      tv.tv_sec = ms / 1000;
      tv.tv_usec = (ms % 1000) * 1000;
      v = select (0, NULL, NULL, NULL, &tv);
      /* The value of the timeout is undefined after the select returns */
    }
  while ((v < 0) && (errno == EINTR));
  if (v < 0)
    error (NULL);
}

int memusage (pid_t pid) {
  char a[SIZE], *p, *q;
  int data, stack;
  int n, v, fd;

  p = a;
  sprintf (p, "/proc/%d/status", pid);
  fd = open (p, O_RDONLY);
  if (fd < 0){
    if (errno == ENOENT){
      return 0;
    } else {
      error (NULL);
    }
  }
  do
    n = read (fd, p, SIZE);
  while ((n < 0) && (errno == EINTR));
  if (n < 0)
    error (NULL);
  do
    v = close (fd);
  while ((v < 0) && (errno == EINTR));
  if (v < 0)
    error (NULL);

  data = stack = 0;
  q = strstr (p, "VmData:");
  if (q != NULL)
    {
      sscanf (q, "%*s %d", &data);
      q = strstr (q, "VmStk:");
      if (q != NULL)
	sscanf (q, "%*s %d\n", &stack);
    }

  return (data + stack);
}

void setlimit (int resource, rlim_t n)
{
  struct rlimit limit;

#ifdef LINUX_HACK
  /* Linux hack: in freebsd the process will   *
   * be killed exactly  after n  seconds. In   *
   * linux the behaviour depends on the kernel *
   * version (before 2.6 the process is killed *
   * after n+1 seconds, in 2.6 is after n.     */
  if (resource == RLIMIT_CPU)
    if (n > 0)
      n--;
#endif

  limit.rlim_cur = limit.rlim_max = n;
  if (setrlimit (resource, &limit) < 0)
    error (NULL);
}

/* Validate the config options, call error () on error */
void validate (void) {
  unsigned int LARGECONST;
  LARGECONST = 4194304;
  if (profile.cpu == 0)
    error ("Cpu time must be greater than zero");
  if (profile.memory >= LARGECONST)
    error ("Memory limit must be smaller than %u", LARGECONST);
  if (profile.core >= LARGECONST)
    error ("Core limit must be smaller than %u", LARGECONST);
  if (profile.stack >= LARGECONST)
    error ("Stack limit must be smaller than %u", LARGECONST);
  if (profile.fsize >= LARGECONST)
    error ("File size limit must be smaller than %u", LARGECONST);
  if (profile.nproc >= 65536)
    error ("Number of process(es) must be smaller than %u", 65536);
  if (profile.clock <= 0)
    error ("Wall clock time must be greater than zero");
  if (profile.clock >= LARGECONST)
    error ("Wall clock time must be smaller than %u", LARGECONST);
  if (profile.uidplus >= LARGECONST)
    error ("uidplus must be smaller than %u", LARGECONST);
  if (profile.nfile > 1024)
    error ("File number limit must be no larger than %u", 1024);
  if (profile.niceness < 10 || profile.niceness > 19)
    error ("Niceness must be between 10 and 19");
  if (profile.gid < 1 || profile.gid > 65535)
    error ("Group id must be no larger than %u", 65535);
}

/* return NULL on failure, or argv + k
   where the command description starts */
char **parse (char **p)
{
  unsigned int *input1, *input2;
  char **string1;
  char *function;
  int state;

  state = PARSE;
  if (*p == NULL)
    state = ERROR;
  else
    for (; state != ERROR;) {
      p++;
      if (*p == NULL) {
	state = ERROR;
	continue;
      }
      if (state == EXECUTE)
	break;
      switch (state) {
      case PARSE:
	state = EAT_INT;
	function = *p;
	if (strcmp (*p, "--cpu") == 0)
	  input1 = (unsigned int *) &profile.cpu;
	else if (strcmp (*p, "--mem") == 0)
	  input1 = (unsigned int *) &profile.memory;
	else if (strcmp (*p, "--uidplus") == 0)
	  input1 = (unsigned int *) &profile.uidplus;
	else if (strcmp (*p, "--core") == 0)
	  input1 = (unsigned int *) &profile.core;
	else if (strcmp (*p, "--nproc") == 0)
	  input1 = (unsigned int *) &profile.nproc;
	else if (strcmp (*p, "--fsize") == 0)
	  input1 = (unsigned int *) &profile.fsize;
	else if (strcmp (*p, "--stack") == 0)
	  input1 = (unsigned int *) &profile.stack;
	else if (strcmp (*p, "--clock") == 0)
	  input1 = (unsigned int *) &profile.clock;
	else if (strcmp (*p, "--nfile") == 0)
	  input1 = (unsigned int *) &profile.nfile;
	else if (strcmp (*p, "--gid") == 0)
	  input1 = (unsigned int *) &profile.gid;
	else if (strcmp (*p, "--niceness") == 0)
	  input1 = (unsigned int *) &profile.niceness;
	else if (strcmp (*p, "--exec") == 0)
	  state = EXECUTE;
	else if (strcmp (*p, "--report_file") == 0) {
	  state = EAT_STRING;
	  string1 = (char **) &profile.report_file; 
	} else if (strcmp (*p, "--chroot_dir") == 0) {
	  state = EAT_STRING;
	  string1 = (char **) &profile.chroot_dir;
	} else if (strcmp (*p, "--exec_dir") == 0) {
	  state = EAT_STRING;
	  string1 = (char **) &profile.exec_dir; 
	} else if (strcmp (*p, "--env_vars") == 0) {
	  state = EAT_STRING;
	  string1 = (char **) &profile.env_vars; 
	} else if (strcmp (*p, "--silent") == 0) {
	  silent = 1;
	  state = PARSE; 
	} else {
	  fprintf (stderr, "error: Invalid option: %s\n", *p);
	  state = ERROR; 
	}
	break;
      case EAT_STRING:
	*string1 = *p;
	state = PARSE;
	break;
      case EAT_2INT:
	if (sscanf (*p, "%u", input2) == 1)
	  state = EAT_INT;
	else {
	  fprintf (stderr,
		   "error: Failed to match the first numeric argument for %s\n",
		   function);
	  state = ERROR;
	}
	break;
      case EAT_INT:
	if (sscanf (*p, "%u", input1) == 1)
	  state = PARSE;
	else {
	  fprintf (stderr,
		   "error: Failed to match the numeric argument for %s\n",
		   function);
	  state = ERROR;
	}
	break;
      default:
	break;
      }
    }
  if (state == ERROR)
    return (NULL);
  else {
    assert (state == EXECUTE);
    validate ();
    return (p);
  }
}

void printusage (char **p)
{
  fprintf (stderr, "\nusage: %s <options> --exec <command>\n", *p);
  fprintf (stderr, "\t\t**ATTENTION: read the security precautions in README**\n");
  fprintf (stderr, "Available options:\n");
  fprintf (stderr, "\t--uidplus      <number>        default: %u\n",
	   pdefault->uidplus);
  fprintf (stderr, "\t--gid          <group id>      Default: %d\n",
	   ((int) pdefault->gid));
  fprintf (stderr, "\t--cpu          <seconds>       Default: %lu second(s)\n",
	   pdefault->cpu);
  fprintf (stderr, "\t--clock        <seconds>       Wall clock timeout (default: %lu)\n",
	   pdefault->clock);
  fprintf (stderr, "\t--mem          <kbytes>        Default: %lu kbyte(s)\n",
	   pdefault->memory);
  fprintf (stderr, "\t--core         <kbytes>        Default: %lu kbyte(s)\n",
	   pdefault->core);
  fprintf (stderr, "\t--stack        <kbytes>        Default: %lu kbyte(s)\n",
	   pdefault->stack);
  fprintf (stderr, "\t--nproc        <number>        Default: %lu proccess(es)\n",
	   pdefault->nproc);
  fprintf (stderr, "\t--fsize        <kbytes>        Default: %lu kbyte(s)\n",
	   pdefault->fsize);
  fprintf (stderr, "\t--nfile        <number>        Default: %lu file pointer(s)\n",
	   pdefault->nfile);
  fprintf (stderr, "\t--niceness     <int>           Default: %d (19=lowest priority, 10=highest)\n",
	   pdefault->niceness);
  fprintf (stderr, "\t--chroot_dir   <dir>           Default: NULL (a full path starting with /)\n");
  fprintf (stderr, "\t--exec_dir     <dir>           Default: NULL (relative to chroot_dir)\n");
  fprintf (stderr, "\t--env_vars     \"X=Y\\nA=B\", PY  Default: inherit calling\n");
  fprintf (stderr, "\t--report_file  <filename>      Supervisor report (relative to current dir; default: stderr)\n");
  fprintf (stderr, "Returns: EXIT_SUCCESS(0) if everything went ok, EXIT_FAILURE otherwise (internal errors, over-limit, etc).\n\n");

#ifdef LINUX_HACK
  fprintf (stderr, "Compiled with LINUX_HACK for RLIMIT_CPU\n");
#endif
}

void wallclock (int v)
{
  if (v != SIGALRM)
    error ("Signal delivered is not SIGALRM");
  mark = RTLE;
  terminate (pid);
}

int main (int argc, char **argv, char **envp)
{
  struct rusage usage;
  char **p;
  int status, mem;
  int tsource, ttarget;
  int v;

  redirect = stderr;
  safe_signal (SIGPIPE, SIG_DFL);

  tsource = time (NULL);
  p = parse (argv);
  if (p == NULL) {
    printusage (argv);
    return (EXIT_FAILURE);
  }


  if (profile.env_vars != NULL) {
    if (strcmp(profile.env_vars, "PY") == 0) { 
      /* shorthand for needed Python environment variables, assuming that
	 the necessary executables, libraries, etc. are in the root of jail */
      char* xnewenvp[] = { "PYTHONIOENCODING=utf_8", "PYTHONHOME=/", "PYTHONPATH=/static", NULL };
      envp = xnewenvp;
    }
    else {
      char * newenvp[100];
      char ** iter = newenvp;
      *iter = strtok (profile.env_vars,"\n");
      while (*iter != NULL) { 
	iter++;
	*iter = strtok (NULL, "\n");
      } 
      envp = newenvp;
    }
  }

  if (profile.report_file != NULL) {
    redirect = fopen (profile.report_file, "w");
    if (redirect == NULL)
      error ("Couldn't open redirection file\n");
  }
      
  pid = fork ();
  if (pid < 0)
    error (NULL);

  if (pid == 0) { /* FORK: slave process that will run the submitted code */

    profile.theuid = profile.uidplus + getpid();

    setlimit (RLIMIT_AS, profile.memory * 1024); 
    setlimit (RLIMIT_DATA, profile.memory * 1024); 
    setlimit (RLIMIT_CORE, profile.core * 1024);
    setlimit (RLIMIT_STACK, profile.stack * 1024);
    setlimit (RLIMIT_FSIZE, profile.fsize * 1024);
    setlimit (RLIMIT_CPU, profile.cpu);
    setlimit (RLIMIT_NOFILE, profile.nfile);
    setlimit (RLIMIT_NPROC, profile.nproc + 1);  /* 1 required by setuid */
    
    if (profile.chroot_dir != NULL && 0 != chdir(profile.chroot_dir)) {
      error ("Could not chdir to chroot dir [%s] while in [%s]\n", profile.chroot_dir, getcwd(NULL, 0));
      kill (getpid (), SIGPIPE);
    }
    
    if (profile.chroot_dir != NULL && chroot(".") != 0) {
      error ("Cannot chroot while in [%s]\n", getcwd(NULL, 0));
      kill (getpid (), SIGPIPE);
    }
    
    if (profile.exec_dir != NULL && 0 != chdir(profile.exec_dir)) {
      error ("Cannot change to rundir");
      kill (getpid (), SIGPIPE);
    }
    
    if (0 != setpriority(PRIO_PROCESS, getpid(), profile.niceness)) {
      error ("Could not set priority");
      kill (getpid (), SIGPIPE);
    }
    
    if (setgid (profile.gid) < 0 || getgid () != profile.gid || profile.gid == 0)
      error ("setgid failed\n");
    
    if (setgroups (0, NULL) < 0 || getgroups (0, NULL) != 0)
      error ("setgroups failed\n");
    
    if (setuid (profile.theuid) < 0 || getuid() != profile.theuid || profile.theuid == 0)
      error ("setuid failed\n");
    
    if (execve (*p, p, envp) < 0) {
      error ("execve error\n");
      kill (getpid (), SIGPIPE);
    }
    /* goodbye process! execve never returns. */
  }
  
  else { /* FORK: supervisor process */
    
    if (signal (SIGALRM, wallclock) == SIG_ERR)
      error ("Couldn't install signal handler");
    
    if (alarm (profile.clock) != 0)
      error ("Couldn't set alarm");

    mark = OK;
    
    /* Poll at INTERVAL ms and determine the maximum *
     * memory usage,  exit when the child terminates */
    
    mem = -1;
    do {
      msleep (INTERVAL);
      mem = max (mem, memusage (pid));
      if (mem > profile.memory) {
	terminate (pid);
	mark = MLE;
      }
      do
	v = wait4 (pid, &status, WNOHANG | WUNTRACED, &usage);
      while ((v < 0) && (errno != EINTR));
      if (v < 0)
	error (NULL);
    } while (v == 0);

    ttarget = time (NULL);
    
    if (mark == MLE)
      printstats ("Memory Limit Exceeded\n");
    else if (mark == RTLE)
      printstats ("Time Limit Exceeded\n");
    else {
      if (WIFEXITED (status) != 0) {
	if (WEXITSTATUS (status) != 0) {
	  if (mark == OK)
	    mark = RETNZ;
	  printstats ("Command exited with non-zero status (%d)\n",
		      WEXITSTATUS (status));
	}
	else
	  printstats ("OK\n");
      }
      else {
	if (WIFSIGNALED (status) != 0) {
	  /* Was killed for a TLE (or was it an OLE) */
	  if (WTERMSIG (status) == SIGKILL)
	    mark = TLE;
	  else if (WTERMSIG (status) == SIGXFSZ)
	    mark = OLE;
	  else if (WTERMSIG (status) == SIGHUP)
	    mark = RF;
	  else if (WTERMSIG (status) == SIGPIPE)
	    mark = IE;
	  else {
	    if (mark == OK)
	      mark = TERM;
	    printstats ("Command terminated by signal (%d: %s)\n",
			WTERMSIG (status),
			name (WTERMSIG (status)));
	  }
	}
	else if (WIFSTOPPED (status) != 0) {
	  if (mark == OK)
	    mark = TERM;
	  printstats ("Command terminated by signal (%d: %s)\n",
		      WSTOPSIG (status), name (WSTOPSIG (status)));
	}
	else
	  printstats ("OK\n");
	
	if (mark == TLE) {
	  /* Adjust the timings... although we know the child   *
	   * was been killed just in the right time seeing 1.99 *
	   * as TLE when the limit is 2 seconds is anoying      */
	  usage.ru_utime.tv_sec = profile.cpu;
	  usage.ru_utime.tv_usec = 0;
	  printstats ("Time Limit Exceeded\n");
	}
	else if (mark == OLE)
	  printstats ("Output Limit Exceeded\n");
	else if (mark == RTLE)
	  printstats ("Time Limit Exceeded\n");
	else if (mark == RF)
	  printstats ("Invalid Function\n");
	else if (mark == IE)
	  printstats ("Internal Error\n");
      }
    }
    printstats ("elapsed time: %d seconds\n", ttarget - tsource);
    if (mem != -1) /* -1: died too fast to measure */
      printstats ("memory usage: %d kbytes\n", mem);
    printstats ("cpu usage: %0.3f seconds\n",
		(float) milliseconds (&usage.ru_utime) / 1000.0);
  } /* end of FORK */

  fclose (redirect);

  if (mark == OK)
    return (EXIT_SUCCESS);
  else
    return (EXIT_FAILURE);
}
