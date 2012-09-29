html-lang
meta-charset
page-title
meta-description
meta-keywords

meta-autor
meta-generator

*header
**meta-extras
**css-extras
**js-extras

*body
** body-header
** body-main
** body-footer
analytics-code

jquery-import
body-bottom


{% block script-end-of-body %}
	<script type="text/javascript">

		$(document).ready(function() {
			{% block jquery-docready %}{% endblock %}
		  });
		$(window).load(function() {
			{% block jquery-winload %}{% endblock %}
		});			
		{% block head-js %}{% endblock %}
	</script>
	
	
