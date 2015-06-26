var data = {
    first_name: "Veit",
    last_name: "Heller",
    nickname: "Elephant",
    age: "20",
    gender: undefined,
    education: "student",
    birthday: true,
    username: "42"
}

validator.config = {
    first_name: 'isAlphaNum',
    age: 'isNumber',
    username: 'isAlphaNum',
    gender: 'isNonEmpty',
    education: 'isDefined',
    birthday: 'isDate'
};

validator.validate(data);
if(validator.hasErrors()){
    print(validator.messages.join("\n"));
};
