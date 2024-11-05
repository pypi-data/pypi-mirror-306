""" Generated file, do not modify """

SCRIPTS_TEMPLATES = {
    'ides': """
<script type="application/javascript" src="{{ config.plugins.pyodide_macros.rebase(base_url) }}/js-per-pages/4_ideRunner-ides.js"></script>
""",
    'ides_test': """
<script type="application/javascript" src="{{ config.plugins.pyodide_macros.rebase(base_url) }}/js-per-pages/5-ideTester-ides_test.js"></script>
""",
    'pyodide': """
<script type="application/javascript" src="{{ config.plugins.pyodide_macros.rebase(base_url) }}/js-per-pages/0_genericPythonSnippets-pyodide.js"></script>
<script type="application/javascript" src="{{ config.plugins.pyodide_macros.rebase(base_url) }}/js-per-pages/1_error-logs-generator-pyodide.js"></script>
<script type="application/javascript" src="{{ config.plugins.pyodide_macros.rebase(base_url) }}/js-per-pages/1_packagesInstaller-pyodide.js"></script>
<script type="application/javascript" src="{{ config.plugins.pyodide_macros.rebase(base_url) }}/js-per-pages/1_runtimeManager-pyodide.js"></script>
<script type="application/javascript" src="{{ config.plugins.pyodide_macros.rebase(base_url) }}/js-per-pages/2_pyodideSectionsRunner-pyodide.js"></script>
<script type="application/javascript" src="{{ config.plugins.pyodide_macros.rebase(base_url) }}/js-per-pages/3_btnRunner-pyodide.js"></script>
<script type="application/javascript" src="{{ config.plugins.pyodide_macros.rebase(base_url) }}/js-per-pages/start-pyodide.js"></script>
""",
    'qcm': """
<script type="application/javascript" src="{{ config.plugins.pyodide_macros.rebase(base_url) }}/js-per-pages/qcms-qcm.js"></script>
""",
    'terms': """
<script type="application/javascript" src="{{ config.plugins.pyodide_macros.rebase(base_url) }}/js-per-pages/3_terminalRunner-terms.js"></script>
""",
}
