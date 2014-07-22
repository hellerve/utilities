//validates the pattern provided; see validatortest for example usage
var validator = {
    types : {},
    messages: [],
    config: {},
    validate: function(data){
        var i, msg, type, checker, result_ok;

        this.messages = [];

        for(i in data){
            if(data.hasOwnProperty(i)){
                type = this.config[i];
                checker = this.types[type];
                if(!type) continue;
                if(!checker)
                    throw{
                        name: "ValidationError",
                        message: "No handler to validate type" + type
                    };
            }
            result_ok = checker.validate(data[i]);
            if(!result_ok){
                msg = "Invalid value for *" + i + "*, " + checker.instructions;
                this.messages.push(msg);
            }
        }
        return this.hasErrors();
    },
    hasErrors: function(){
        return this.messages.length !== 0;
    }
};

validator.types.isNonEmpty = {
    validate: function(value){
        return value !== "";
    },
    instructions: "The value cannot be empty"
};

validator.types.isNumber = {
    validate: function(value){
        return !isNaN(value);
    },
    instructions: "the value can only be a valid number, e.g. 1, 3.14 or 2014"
};

validator.types.isAlphaNum = {
    validate: function(value){
        return !/[^a-z0-9]/i.test(value);
    },
    instructions: "the value can only contain characters and numbers, no special symbols"
};

validator.types.isAlpha = {
    validate: function(value){
        return !/[^a-z]/i.test(value);
    },
    instructions: "the value can only contain characters"
};

validator.types.isDefined = {
    validate: function(value){
        return value !== undefined;
    },
    instructions: "the value cannot be undefined"
};

validator.types.isBool = {
    validate: function(value){
        return typeof value === "boolean";
    },
    instructions: "the value must be boolean"
};

validator.types.isTrue = {
    validate: function(value){
        return value === true;
    },
    instructions: "the value must be true"
};

validator.types.isFalse = {
    validate: function(value){
        return value === false;
    },
    instructions: "the value must be false"
};

validator.types.isDate = {
    validate: function(value){
        date = value.split(".");
        return date.length() == 3 && date[0] < 32 && date[0] > 0 && 
               date[1] < 12 && date[1] > 0 && date[2] > 0;
    },
    instructions: "the value must have a date format"
};

/*
validator.types.isLongerThanEight = {
    validate: function(value){
        return value.length > 8;
    },
    instructions: "the value must be longer than eight symbols"
};

validator.types.isLongerThanSixteen = {
    validate: function(value){
        return value.length > 16;
    },
    instructions: "the value must be longer than sixteen symbols"
};*/
