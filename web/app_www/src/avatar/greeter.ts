// tsc greeter.ts -> greeter.js
// rollup

export class Student {
    fullName: string;
    constructor(
      public firstName: string,
      public middleInitial: string,
      public lastName: string
    ) {
      this.fullName = firstName + " " + middleInitial + " " + lastName;
    }
}
  
export interface Person {
    firstName: string;
    lastName: string;
 }
  
export function greeter(person: Person) {
  return "Hello, " + person.firstName + " " + person.lastName;
}
  
let user = new Student("Jane", "M.", "User");
document.body.textContent = greeter(user);