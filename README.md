# ShredLang 🏂

ShredLang is a custom programming language inspired by snowboarding culture, designed as part of a project to explore language design and interpreter implementation.

## Features

### 🏔️ Core Language Features
- **Variable Declaration:** Use `trick` to declare variables (e.g., `trick speed = 10;`).
- **Conditionals:** Use `carve` to branch logic (e.g., `carve(speed > 15) { ... }`).
- **Loops:** Use `spin` to iterate actions (e.g., `spin(3 times) { ... }`).
- **Printing:** Use `shout` to print messages (e.g., `shout("Shredding the slopes!");`).
- **Error Handling:** Use `bail` to raise runtime errors (e.g., `bail("Speed too high!");`).

### 📜 Example Code

#### Example 1: Basic Loop with Conditionals
```shd
strap_in
    trick speed = 5;
    spin(3 times)
    {
        carve(spin_iteration == 1)
        {
            shout("Yooo spinning with " + speed + " speed! Spin #" + spin_iteration + " done!");
        }
        carve(spin_iteration > 1)
        {
            shout("This ain't my first time shredding the slopes, this is my spin number " + spin_iteration + "!");
        }
    }
    speed = 20;
    shout("My speed is now " + speed + ", I'm going too fast now!");
unstrap
