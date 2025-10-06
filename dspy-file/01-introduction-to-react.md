---{
  "title": "Introduction to React",
  "source_url": "https://fullstackopen.com/en/part1/introduction_to_react",
  "crawl_timestamp": "2025-10-04T19:15:38Z",
  "checksum": "31ec909f2d98ca6a46b641c72d697b42019c4aad14af4a3947cc73937bfda33a"
}
---[Skip to content](../part1/01-introduction-to-react-course-main-content.md)
[{() => fs}](https://fullstackopen.com/en/)

- [About course](../about/01-about.md)
- [Course contents](../#course-contents/01-course-contents.md)
- [FAQ](../faq/01-faq.md)
- [Partners](../companies/01-companies.md)
- [Challenge](../challenge/01-challenge.md)
[Search from the material](../search/01-search.md)Toggle dark theme
Select languageSuomi English 中文 Español Français Português(BR)

[Fullstack](../#course-contents/01-course-contents.md)
[Part 1](../part1/01-part1.md)
Introduction to React
a Introduction to React

- [Component](../part1/01-introduction-to-react-component.md)
- [JSX](../part1/01-introduction-to-react-jsx.md)
- [Multiple components](../part1/01-introduction-to-react-multiple-components.md)
- [props: passing data to components](../part1/01-introduction-to-react-props-passing-data-to-components.md)
- [Possible error message](../part1/01-introduction-to-react-possible-error-message.md)
- [Some notes](../part1/01-introduction-to-react-some-notes.md)
- [Do not render objects](../part1/01-introduction-to-react-do-not-render-objects.md)
- [Exercises 1.1.-1.2.](../part1/01-introduction-to-react-exercises-1-1-1-2.md)


[b JavaScript](../part1/01-java-script.md)[c Component state, event handlers](../part1/01-component-state-event-handlers.md)[d A more complex state, debugging React apps](../part1/01-a-more-complex-state-debugging-react-apps.md)
a
# Introduction to React
We will now start getting familiar with probably the most important topic of this course, namely the
The easiest way to get started by far is by using a tool called
Let's create a new application using the _create-vite_ tool:

```
npm create vite@latestcopy
```

Let's answer the questions presented by the tool as follows:
![create-vite tool selection view, where the project is named part1, the framework is React, the variant is JavaScript, and all other questions are answered with No](../assets/ebf7abe0b50c05ce.png)
We have now created an application named _part1_. The tool could have also installed the required dependencies and started the application automatically if we had answered "Yes" to the question "Install with npm and start now?" However, we will perform these steps manually so we can see how they are done.
Next, let's move into the application's directory and install the required libraries:

```
cd part1
npm installcopy
```

The application is started as follows:

```
npm run devcopy
```

The console says that the application has started on localhost port 5173, i.e. the address
![screenshot of the console running vite on localhost 5173](../assets/16ac5c4662fde232.png)
Vite starts the application
Open the browser and a text editor so that you can view the code as well as the webpage at the same time on the screen:
![screenshot of vite initial webpage and file structure on vs code](../assets/b180e16bca43a0bb.png)
The code of the application resides in the _src_ folder. Let's simplify the default code such that the contents of the file main.jsx looks like this:

```
import ReactDOM from 'react-dom/client'

import App from './App'

ReactDOM.createRoot(document.getElementById('root')).render(<App />)copy
```

and file _App.jsx_ looks like this

```
const App = () => {
  return (
    <div>
      <p>Hello world</p>
    </div>
  )
}

export default Appcopy
```

The files _App.css_ and _index.css_ , and the directory _assets_ may be deleted as they are not needed in our application right now.
### Component
The file _App.jsx_ now defines a _App_. The command on the final line of file _main.jsx_

```
ReactDOM.createRoot(document.getElementById('root')).render(<App />)copy
```

renders its contents into the _div_ -element, defined in the file _index.html_ , having the _id_ value 'root'.
By default, the file _index.html_ doesn't contain any HTML markup that is visible to us in the browser:

```
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>part1</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>copy
```

You can try adding there some HTML to the file. However, when using React, all content that needs to be rendered is usually defined as React components.
Let's take a closer look at the code defining the component:

```
const App = () => (
  <div>
    <p>Hello world</p>
  </div>
)copy
```

As you probably guessed, the component will be rendered as a _div_ -tag, which wraps a _p_ -tag containing the text _Hello world_.
Technically the component is defined as a JavaScript function. The following is a function (which does not receive any parameters):

```
() => (
  <div>
    <p>Hello world</p>
  </div>
)copy
```

The function is then assigned to a constant variable _App_ :

```
const App = ...copy
```

There are a few ways to define functions in JavaScript. Here we will use
Because the function consists of only a single expression we have used a shorthand, which represents this piece of code:

```
const App = () => {
  return (
    <div>
      <p>Hello world</p>
    </div>
  )
}copy
```

In other words, the function returns the value of the expression.
The function defining the component may contain any kind of JavaScript code. Modify your component to be as follows:

```
const App = () => {
  console.log('Hello from component')
  return (
    <div>
      <p>Hello world</p>
    </div>
  )
}

export default Appcopy
```

and observe what happens in the browser console
![browser console showing console log with arrow to "Hello from component"](../assets/3563adcf0fde2f6c.png)
The first rule of frontend web development:
> _keep the console open all the time_
Let us repeat this together: _I promise to keep the console open all the time_ during this course, and for the rest of my life when I'm doing web development.
It is also possible to render dynamic content inside of a component.
Modify the component as follows:

```
const App = () => {
  const now = new Date()
  const a = 10
  const b = 20
  console.log(now, a+b)

  return (
    <div>
      <p>Hello world, it is {now.toString()}</p>
      <p>
        {a} plus {b} is {a + b}
      </p>
    </div>
  )
}copy
```

Any JavaScript code within the curly braces is evaluated and the result of this evaluation is embedded into the defined place in the HTML produced by the component.
Note that you should not remove the line at the bottom of the component

```
export default Appcopy
```

The export is not shown in most of the examples of the course material. Without the export the component and the whole app breaks down.
Did you remember your promise to keep the console open? What was printed out there?
### JSX
It seems like React components are returning HTML markup. However, this is not the case. The layout of React components is mostly written using
After compiling, our application looks like this:

```
const App = () => {
  const now = new Date()
  const a = 10
  const b = 20
  return React.createElement(
    'div',
    null,
    React.createElement(
      'p', null, 'Hello world, it is ', now.toString()
    ),
    React.createElement(
      'p', null, a, ' plus ', b, ' is ', a + b
    )
  )
}copy
```

The compilation is handled by _Vite_ are configured to compile automatically. We will learn more about this topic in [part 7](../part7/01-part7.md) of this course.
It is also possible to write React as "pure JavaScript" without using JSX. Although, nobody with a sound mind would do so.
In practice, JSX is much like HTML with the distinction that with JSX you can easily embed dynamic content by writing appropriate JavaScript within curly braces. The idea of JSX is quite similar to many templating languages, such as Thymeleaf used along with Java Spring, which are used on servers.
JSX is "

```
<br>copy
```

but when writing JSX, the tag needs to be closed:

```
<br />copy
```

### Multiple components
Let's modify the file _App.jsx_ as follows:

```
const Hello = () => {  return (    <div>      <p>Hello world</p>    </div>  )}
const App = () => {
  return (
    <div>
      <h1>Greetings</h1>
      <Hello />    </div>
  )
}copy
```

We have defined a new component _Hello_ and used it inside the component _App_. Naturally, a component can be used multiple times:

```
const App = () => {
  return (
    <div>
      <h1>Greetings</h1>
      <Hello />
      <Hello />      <Hello />    </div>
  )
}copy
```

**NB** : _export_ at the bottom is left out in these _examples_ , now and in the future. It is still needed for the code to work
Writing components with React is easy, and by combining components, even a more complex application can be kept fairly maintainable. Indeed, a core philosophy of React is composing applications from many specialized reusable components.
Another strong convention is the idea of a _root component_ called _App_ at the top of the component tree of the application. Nevertheless, as we will learn in [part 6](../part6/01-part6.md), there are situations where the component _App_ is not exactly the root, but is wrapped within an appropriate utility component.
### props: passing data to components
It is possible to pass data to components using so-called
Let's modify the component _Hello_ as follows:

```
const Hello = (props) => {  return (
    <div>
      <p>Hello {props.name}</p>    </div>
  )
}copy
```

Now the function defining the component has a parameter props. As an argument, the parameter receives an object, which has fields corresponding to all the "props" the user of the component defines.
The props are defined as follows:

```
const App = () => {
  return (
    <div>
      <h1>Greetings</h1>
      <Hello name='George' />      <Hello name='Daisy' />    </div>
  )
}copy
```

There can be an arbitrary number of props and their values can be "hard-coded" strings or the results of JavaScript expressions. If the value of the prop is achieved using JavaScript it must be wrapped with curly braces.
Let's modify the code so that the component _Hello_ uses two props:

```
const Hello = (props) => {
  console.log(props)  return (
    <div>
      <p>
        Hello {props.name}, you are {props.age} years old      </p>
    </div>
  )
}

const App = () => {
  const name = 'Peter'  const age = 10
  return (
    <div>
      <h1>Greetings</h1>
      <Hello name='Maya' age={26 + 10} />      <Hello name={name} age={age} />    </div>
  )
}copy
```

The props sent by the component _App_ are the values of the variables, the result of the evaluation of the sum expression and a regular string.
Component _Hello_ also logs the value of the object props to the console.
I really hope your console was open. If it was not, remember what you promised:
> _I promise to keep the console open all the time during this course, and for the rest of my life when I'm doing web development_
Software development is hard. It gets even harder if one is not using all the possible available tools such as the web-console and debug printing with _console.log_. Professionals use both _all the time_ and there is no single reason why a beginner should not adopt the use of these wonderful helper methods that will make their life so much easier.
### Possible error message
If your project has React version 18 or earlier installed, you may receive the following error message at this point:
![screenshot of vs code showing eslint error: "name is missing in props validation"](../assets/3fb2e46c4acbf771.png)
It's not an actual error, but a warning caused by the _eslint.config.js_ the next line

```
export default [
  { ignores: ['dist'] },
  {
    files: ['**/*.{js,jsx}'],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
      parserOptions: {
        ecmaVersion: 'latest',
        ecmaFeatures: { jsx: true },
        sourceType: 'module',
      },
    },
    settings: { react: { version: '18.3' } },
    plugins: {
      react,
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
    },
    rules: {
      ...js.configs.recommended.rules,
      ...react.configs.recommended.rules,
      ...react.configs['jsx-runtime'].rules,
      ...reactHooks.configs.recommended.rules,
      'react/jsx-no-target-blank': 'off',
      'react-refresh/only-export-components': [
        'warn',
        { allowConstantExport: true },
      ],
      'react/prop-types': 0,    },
  },
]copy
```

We will get to know ESLint in more detail [in part 3](../part3/01-validation-and-es-lint-lint.md).
### Some notes
React has been configured to generate quite clear error messages. Despite this, you should, at least in the beginning, advance in **very small steps** and make sure that every change works as desired.
**The console should always be open**. If the browser reports errors, it is not advisable to continue writing more code, hoping for miracles. You should instead try to understand the cause of the error and, for example, go back to the previous working state:
![screenshot of undefined prop error](../assets/14ac40c3a5b59bad.png)
As we already mentioned, when programming with React, it is possible and worthwhile to write _console.log()_ commands (which print to the console) within your code.
Also, keep in mind that **First letter of React component names must be capitalized**. If you try defining a component as follows:

```
const footer = () => {
  return (
    <div>
      greeting app created by <a href='https://github.com/mluukkai'>mluukkai</a>
    </div>
  )
}copy
```

and use it like this

```
const App = () => {
  return (
    <div>
      <h1>Greetings</h1>
      <Hello name='Maya' age={26 + 10} />
      <footer />    </div>
  )
}copy
```

the page is not going to display the content defined within the footer component, and instead React only creates an empty _div_ -element defined in the Footer component, which is rendered on the page.
Note that the content of a React component (usually) needs to contain **one root element**. If we, for example, try to define the component _App_ without the outermost _div_ -element:

```
const App = () => {
  return (
    <h1>Greetings</h1>
    <Hello name='Maya' age={26 + 10} />
    <Footer />
  )
}copy
```

the result is an error message.
![multiple root elements error screenshot](../assets/8e7bdbc63cd8ebb1.png)
Using a root element is not the only working option. An _array_ of components is also a valid solution:

```
const App = () => {
  return [
    <h1>Greetings</h1>,
    <Hello name='Maya' age={26 + 10} />,
    <Footer />
  ]
}copy
```

However, when defining the root component of the application this is not a particularly wise thing to do, and it makes the code look a bit ugly.
Because the root element is stipulated, we have "extra" div elements in the DOM tree. This can be avoided by using

```
const App = () => {
  const name = 'Peter'
  const age = 10

  return (
    <>
      <h1>Greetings</h1>
      <Hello name='Maya' age={26 + 10} />
      <Hello name={name} age={age} />
      <Footer />
    </>
  )
}copy
```

It now compiles successfully, and the DOM generated by React no longer contains the extra div element.
### Do not render objects
Consider an application that prints the names and ages of our friends on the screen:

```
const App = () => {
  const friends = [
    { name: 'Peter', age: 4 },
    { name: 'Maya', age: 10 },
  ]

  return (
    <div>
      <p>{friends[0]}</p>
      <p>{friends[1]}</p>
    </div>
  )
}

export default Appcopy
```

However, nothing appears on the screen. I've been trying to find a problem in the code for 15 minutes, but I can't figure out where the problem could be.
I finally remember the promise we made
> _I promise to keep the console open all the time during this course, and for the rest of my life when I'm doing web development_
The console screams in red:
![devtools showing error with highlight around "Objects are not valid as a React child"](../assets/2d297e1eec19b3a2.png)
The core of the problem is _Objects are not valid as a React child_ , i.e. the application tries to render _objects_ and it fails again.
The code tries to render the information of one friend as follows

```
<p>{friends[0]}</p>copy
```

and this causes a problem because the item to be rendered in the braces is an object.

```
{ name: 'Peter', age: 4 }copy
```

In React, the individual things rendered in braces must be primitive values, such as numbers or strings.
The fix is ​​as follows

```
const App = () => {
  const friends = [
    { name: 'Peter', age: 4 },
    { name: 'Maya', age: 10 },
  ]

  return (
    <div>
      <p>{friends[0].name} {friends[0].age}</p>
      <p>{friends[1].name} {friends[1].age}</p>
    </div>
  )
}

export default Appcopy
```

So now the friend's name is rendered separately inside the curly braces

```
{friends[0].name}copy
```

and age

```
{friends[0].age}copy
```

After correcting the error, you should clear the console error messages by pressing 🚫 and then reload the page content and make sure that no error messages are displayed.
A small additional note to the previous one. React also allows arrays to be rendered _if_ the array contains values ​​that are eligible for rendering (such as numbers or strings). So the following program would work, although the result might not be what we want:

```
const App = () => {
  const friends = [ 'Peter', 'Maya']

  return (
    <div>
      <p>{friends}</p>
    </div>
  )
}copy
```

In this part, it is not even worth trying to use the direct rendering of the tables, we will come back to it in the next part.
### Exercises 1.1.-1.2
The exercises are submitted via GitHub, and by marking the exercises as done in the "my submissions" tab of the
The exercises are submitted **one part at a time**. When you have submitted the exercises for a part of the course you can no longer submit undone exercises for the same part.
Note that in this part, there are [more exercises](../part1/01-a-more-complex-state-debugging-react-apps-exercises-1-6-1-14.md) besides those found below. _Do not submit your work_ until you have completed all of the exercises you want to submit for the part.
You may submit all the exercises of this course into the same repository, or use multiple repositories. If you submit exercises of different parts into the same repository, please use a sensible naming scheme for the directories.
One very functional file structure for the submission repository is as follows:

```
part0
part1
  courseinfo
  unicafe
  anecdotes
part2
  phonebook
  countriescopy
```

See this
For each part of the course, there is a directory, which further branches into directories containing a series of exercises, like "unicafe" for part 1.
Most of the exercises of the course build a larger application, eg. courseinfo, unicafe and anecdotes in this part, bit by bit. It is enough to submit the completed application. You can make a commit after each exercise, but that is not compulsory. For example the course info app is built in exercises 1.1.-1.5. It is just the end result after 1.5 that you need to submit!
For each web application for a series of exercises, it is recommended to submit all files relating to that application, except for the directory _node_modules_.
#### 1.1: Course Information, step 1
_The application that we will start working on in this exercise will be further developed in a few of the following exercises. In this and other upcoming exercise sets in this course, it is enough to only submit the final state of the application. If desired, you may also create a commit for each exercise of the series, but this is entirely optional._
Use Vite to initialize a new application. Modify _main.jsx_ to match the following

```
import ReactDOM from 'react-dom/client'

import App from './App'

ReactDOM.createRoot(document.getElementById('root')).render(<App />)copy
```

and _App.jsx_ to match the following

```
const App = () => {
  const course = 'Half Stack application development'
  const part1 = 'Fundamentals of React'
  const exercises1 = 10
  const part2 = 'Using props to pass data'
  const exercises2 = 7
  const part3 = 'State of a component'
  const exercises3 = 14

  return (
    <div>
      <h1>{course}</h1>
      <p>
        {part1} {exercises1}
      </p>
      <p>
        {part2} {exercises2}
      </p>
      <p>
        {part3} {exercises3}
      </p>
      <p>Number of exercises {exercises1 + exercises2 + exercises3}</p>
    </div>
  )
}

export default Appcopy
```

and remove the extra files _App.css_ and _index.css_ , also remove the directory _assets_.
Unfortunately, the entire application is in the same component. Refactor the code so that it consists of three new components: _Header_ , _Content_ , and _Total_. All data still resides in the _App_ component, which passes the necessary data to each component using _props_. _Header_ takes care of rendering the name of the course, _Content_ renders the parts and their number of exercises and _Total_ renders the total number of exercises.
Define the new components in the file _App.jsx_.
The _App_ component's body will approximately be as follows:

```
const App = () => {
  // const-definitions

  return (
    <div>
      <Header course={course} />
      <Content ... />
      <Total ... />
    </div>
  )
}copy
```

**WARNING** Don't try to program all the components concurrently, because that will almost certainly break down the whole app. Proceed in small steps, first make e.g. the component _Header_ and only when it works for sure, you could proceed to the next component.
Careful, small-step progress may seem slow, but it is actually _by far the fastest_ way to progress. Famous software developer Robert "Uncle Bob" Martin has stated
> _"The only way to go fast, is to go well"_
that is, according to Martin, careful progress with small steps is even the only way to be fast.
#### 1.2: Course Information, step 2
Refactor the _Content_ component so that it does not render any names of parts or their number of exercises by itself. Instead, it only renders three _Part_ components of which each renders the name and number of exercises of one part.

```
const Content = ... {
  return (
    <div>
      <Part .../>
      <Part .../>
      <Part .../>
    </div>
  )
}copy
```

Our application passes on information in quite a primitive way at the moment, since it is based on individual variables. We shall fix that in [part 2](../part2/01-part2.md), but before that, let's go to part1b to learn about JavaScript.
[Part 0 **Previous part**](../part0/01-part0.md)[Part 1b **Next part**](../part1/01-java-script.md)
[About course](../about/01-about.md)[Course contents](../#course-contents/01-course-contents.md)[FAQ](../faq/01-faq.md)[Partners](../companies/01-companies.md)[Challenge](../challenge/01-challenge.md)
