# React Component Refactoring Exercise Report

## Overview

This exercise involves refactoring a React app into a component-based structure. The `App` component is decomposed into `Header`, `Content`, and `Total`, with `Content` further split into `Part` components. Data flows from `App` to child components via props, ensuring modular and maintainable code.

---

## Key Concepts

- **Component Decomposition**: Breaking down the UI into reusable components.
- **Prop Passing**: Transferring data (e.g., course name, exercises) from parent to child components.
- **Modular Structure**: Separating concerns into distinct components (Header, Part, Total).
- **JSX Rendering**: Using JSX to dynamically render component outputs.
- **Data Aggregation**: Calculating totals in parent components before passing data to children.

---

## Practical Steps

1. Create `Header` component to display the course name via the `course` prop.
2. Implement `Part` component to render part details (name and exercises) using `part` and `exercises` props.
3. Build `Content` component to pass three `Part` components with their respective data.
4. Develop `Total` component to calculate and display the sum of all exercises via the `totalExercises` prop.
5. Update `App` to aggregate data (e.g., sum of exercises) and pass it to child components.
6. Ensure all components are defined before use in JSX to avoid runtime errors.

---

## Common Pitfalls

- Incorrectly passing props, leading to undefined values in child components.
- Forgetting to define components before using them in JSX.
- Failing to aggregate data in `App` before passing it to child components.
- Mixing direct rendering (e.g., hard-coded values) with component-based rendering.
- Not validating prop types, which can cause runtime errors.

---

## References

- React documentation on props and child components.
- Example code from the problem statement for component structure.
- Best practices for modular React application design.
