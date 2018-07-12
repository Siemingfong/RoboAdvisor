window.addEventListener('load', function() {
    var editor;
    // Configure styles
    ContentTools.StylePalette.add([
        new ContentTools.Style('Author', 'author', ['p'])
    ]);

    // Select the editable regions
    editor = ContentTools.EditorApp.get();
    editor.init('*[data-editable]', 'data-name');
});