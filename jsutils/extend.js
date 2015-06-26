//extends a child(second argument) with a parents'(first argument) own property(no deep copy)
function extend(parent, child){
    var i;
    child = child || {};
    for(i in parent)
        if(parent.hasOwnProperty(i))
            child[i] = parent[i];
    return child;
}

//extends a child(second argument) with a parents'(first argument) own property(deep copy)
function extendDeep(parent, child){
    var i,
        toStr = Object.prototype.toString,
        astr = "[object Array]";

    child = child || {};
    for(i in parent)
        if(parent.hasOwnProperty(i))
            if(typeof parent[i] === "object"){
                child[i] = (toStr.call(parent[i]) === astr) ? [] : {};
                extendDeep(parent[i], child[i]);
            } else
                child[i] = parent[i];
    return child;
}

//creates a child from the arguments supplied that inherits all 
//the properties of the parameters
function mixin(){
    var arg, prop, child = {};
    for(arg = 0; arg < arguments.length; arg += 1)
        for(prop in arguments[arg])
            if(arguments[arg].hasOwnProperty(prop))
                child[prop] = argument[arg][prop];
    return child;
}
