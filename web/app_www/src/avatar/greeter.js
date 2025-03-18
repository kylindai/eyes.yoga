"use strict";
// $ tsc src/avatar/greeter.ts --outDir static/avatar/js --module esnext --moduleResolution node
Object.defineProperty(exports, "__esModule", { value: true });
exports.greeter = exports.Student = void 0;
class Student {
    constructor(firstName, middleInitial, lastName) {
        this.firstName = firstName;
        this.middleInitial = middleInitial;
        this.lastName = lastName;
        this.fullName = firstName + " " + middleInitial + " " + lastName;
    }
}
exports.Student = Student;
function greeter(person) {
    return "Hello, " + person.firstName + " " + person.lastName;
}
exports.greeter = greeter;
