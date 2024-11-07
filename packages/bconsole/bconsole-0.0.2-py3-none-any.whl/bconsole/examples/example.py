from bconsole import Console, Foreground

console = Console()

console.print("Hello World!", Foreground.make_rgb(255, 128, 30))
console.input("What is your name?")
console.options("Do you like the color red?")  # defaults to yes/no
console.options("Which animal do you prefer, cats or dogs?", options=["cats", "dogs"])

try:
    console.options(
        "Choose a programming language: Python or PHP", options=["Python", "PHP"]
    )
except ValueError as e:
    console.error(e)

console.action("I'm doing something important!")
console.error("Something went wrong!")
console.panic("Something went really wrong!", hint="Maybe you should try again?")
