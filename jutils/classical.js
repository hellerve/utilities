//lets an child(first argument) inherit from the parent(second argument)
function inherit(C, P){
    var F = function(){};
    F.prototype = P.prototype;
    C.prototype = new F();
    C.uber = P.prototype;
    C.prototype.constructor = C;
}

//Creates a class-like object with optional parent and properties
var classical = function(Parent, props){
    var Child, F, i;

    Child = function(){
        if(Child.uber && Child.uber.hasOwnProperty("__construct"))
            Child.uber.__construct.apply(this, arguments);
        if(Child.prototype.hasOwnProperty("__construct"))
            Child.prototype.__construct.apply(this, arguments);
    };

    Parent = Parent || Object;
    F = function(){};
    F.prototype = Parent.prototype;
    Child.prototype.constructor = Child;

    for(i in props)
        if(props.hasOwnProperty(i))
            Child.prototype[i] = props[i];

    return Child;
}
