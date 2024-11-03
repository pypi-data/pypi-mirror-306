/*
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
*/



function getTheme() {
  // automatically load current palette
  const palette = __md_get("__palette")
  let curPalette = palette===null ? CONFIG.ACE_COLOR_THEME.customThemeDefaultKey
                                  : palette.color["scheme"]

  const style = CONFIG.ACE_COLOR_THEME.customTheme[curPalette]
  return "ace/theme/" + CONFIG.ACE_COLOR_THEME.aceStyle[style];
}




/** Gather color theme data (once only). */
;(function initiatePage(){

  // Create ACE theme:
  const getRGBChannels=colorString=>[
      colorString.slice(1, 3), colorString.slice(3, 5), colorString.slice(5, 7),
  ].map(s=>parseInt(s,16));


  const bodyStyles = window.getComputedStyle(document.body);
  const primaryColor = bodyStyles.getPropertyValue("--md-primary-fg-color");

  document.documentElement.style.setProperty(
      "--main-color", getRGBChannels(primaryColor)
  );

  const _slate = document.getElementById("ace_palette").dataset.aceDarkMode;
  const _default = document.getElementById("ace_palette").dataset.aceLightMode;
  let [default_ace_style, customLightTheme] = _default.split("|")
  let [slate_ace_style,   customDarkTheme] = _slate.split("|")
  customLightTheme ||= "default"
  customDarkTheme  ||= "slate"

  // Correspondance between the custom and the classic palettes
  CONFIG.ACE_COLOR_THEME.customThemeDefaultKey = customLightTheme
  CONFIG.ACE_COLOR_THEME.customTheme = {
      [customLightTheme]: "default",
      [customDarkTheme]: "slate",
  };

  // Get ACE style
  CONFIG.ACE_COLOR_THEME.aceStyle = {
      default: default_ace_style,
      slate: slate_ace_style,
  };



  //-----------------------------------------------------------------


  // Setup actions to perform each time the document has changed (page load)

  // Initialize the content of each IDE in the page
  CONFIG.element.allEditors.forEach(id=>{
    $(`[id^=global_${ id }]`).each(function(){
      const editorId = this.id.slice('global_'.length)
      const ide = id=="editor_" ? new CONFIG.CLASSES_POOL.Ide(editorId)
                                : new CONFIG.CLASSES_POOL.IdeTester(editorId)
      ide.build()
    })
  })


  // Setup independent terminals, if any
  $("div[id^=term_only_]").each(function(){
      const termHandler = new CONFIG.CLASSES_POOL.Terminal(this.id)
      termHandler.build()
  })


  // Setup py_btns, if any
  $("[id^=btn_only_]").each(function(){
      const btn = new CONFIG.CLASSES_POOL.PyBtn(this.id)
      btn.build()
  })


  // Setup auto running elements, if any
  $("[id^=auto_run_]").each(function(){
    const btn = new CONFIG.CLASSES_POOL.PyBtn(this.id)
    btn.build()
})


  /**Setup reactivity for the day/night button.
   * NOTE: yet again, jQuery didn't work on a "change" event.
   * */
  document
    .querySelector("[data-md-color-scheme]")
    .addEventListener("change", _=>{
      jsLogger("[Paint_ACEs]")

      const theme = getTheme();
      for(const id of CONFIG.element.allEditors){
        for (let theEditor of document.querySelectorAll(`div[id^="${ id }"]`)) {
          let editor = ace.edit(theEditor.id);
          editor.setTheme(theme);
          editor.getSession().setMode("ace/mode/python");
        }
      }
    });

  if(CONFIG.CLASSES_POOL.Qcm){
    subscribeWhenReady("QCM", function(){
      jsLogger('[QCM]')
      CONFIG.CLASSES_POOL.Qcm.buildQcms()
    }, {now:true, runOnly:true})
  }

})()
