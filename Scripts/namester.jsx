function GetComp(title) {
    for (var i = 1; i <= app.project.numItems; i++) {
        if ((app.project.item(i) instanceof CompItem) && (app.project.item(i).name === title)) {
            return app.project.item(i);
        }
    }

    alert("Comp cannot be found.");
    return null;
}

function GetLayer(comp, title) {
    for (var i = 1; i <= comp.layers.length; i++) {
        if (comp.layers[i].name === title) {
            return comp.layers[i];
        }
    }

    alert("Layer cannot be found.");
    return null;
}

function OpenFile() {
    var myFile = File.openDialog("Please select input text file.");
    if (myFile == null) {
        return
    }
    
    // open file
    var fileOK = myFile.open("r");
    if (fileOK) {
        return myFile;
    }

    alert("Error when opening file.");
    return null;
}

function main() {
    var comp = GetComp("Main");
    if (comp == null) {
        return;
    }
    
    var layer = GetLayer(comp, "Name");
    if (layer == null) {
        return;
    }
    
    f = OpenFile();
    var outputFolder = Folder.selectDialog("Select a render output folder...");

    var text;
    while (!f.eof) {
        text = f.readln();
        layer.property("Source Text").setValue(text);
        item = app.project.renderQueue.items.add(comp);
        om = item.outputModule(1);
        output_name = text.split('.').join('-');
        om.file = new File(outputFolder.toString() + "/" + "what_happened_cart_crash_" + output_name);
        //app.project.renderQueue.queueInAME(true);
        app.project.renderQueue.render();
    }

}

main();

