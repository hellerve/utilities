//implements a pseudo-platform-independent event handler
function handle(callback){
    return function(e){
        var src, parts;

        e = e || window.event;
        src = e.target || e.srcElement;
        
        callback(src);

        if(typeof e.stopPropagation === "function")
            e.stopPropagation();
        if(typeof e.cancelBubble !== "undefined")
            e.cancelBubble = true;

        if(typeof e.preventDefault === "function")
            e.preventDefault();
        if(typeof e.returnValue !== "undefined")
            e.returnValue = false;
    }
}
