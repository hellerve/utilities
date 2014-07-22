//implements the for each loop
function forEach(elements, callback){
    for(var i = 0; i < elements.length; i++)
        callback(elements[i]);
}

//implements a negating function
function negation(fun){
    return functions(){
        return !fun.apply(null, arguments);
    };
}

//implements the reduction function
function reduce(fun, base, elements){
    forEach(elements, function(e){
        base = fun(base, e);
    });
    return base;
}

//an alias for reduce()
function fold(fun, base, elements){
    return reduce(fun, base, elements);
}

//implements the map function
function map(fun, elements){
    var result = [];
    forEach(elements, function(e){
        result.push(fun(e));
    });
    return result;
}
