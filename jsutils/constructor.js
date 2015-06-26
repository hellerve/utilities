///Implements the sandbox pattern
function SandboxConstruct(){
    var args = Array.prototype.slice.call(arguments),
        callback = args.pop(),
        modules = (args[0] && typeof args[0] == "string") ? args : args[0],
        i;

    if(!(this instanceof SandboxConstruct))
        return new SandboxConstruct(modules, callback);

    if(!modules || modules === '*'){
        modules = [];
        for(i in SandboxConstruct.modules)
            if(SandboxConstruct.modules.hasOwnProperty(i))
                modules.push(i);
    }

    for(i = 0; i < modules.length; i++)
        SandboxConstruct.modules[modules[i]](this);

    callback(this);
};

SandboxConstruct.prototype = {
    VERSION: ['0', '1', '0'],
    DESC: "Implements the sandbox pattern",
    getVersion: function getVersion(){
        return this.VERSION.join(".");
    }
}
