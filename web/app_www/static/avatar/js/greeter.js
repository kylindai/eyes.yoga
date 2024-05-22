"use strict";
// tsc greeter.ts -> greeter.js
// rollup
Object.defineProperty(exports, "__esModule", { value: true });
exports.greeter = exports.Student = void 0;
var Student = /** @class */ (function () {
    function Student(firstName, middleInitial, lastName) {
        this.firstName = firstName;
        this.middleInitial = middleInitial;
        this.lastName = lastName;
        this.fullName = firstName + " " + middleInitial + " " + lastName;
    }
    return Student;
}());
exports.Student = Student;
function greeter(person) {
    return "Hello, " + person.firstName + " " + person.lastName;
}
exports.greeter = greeter;
var user = new Student("Jane", "M.", "User");
document.body.textContent = greeter(user);
