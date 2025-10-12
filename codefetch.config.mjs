/** @type {import('codefetch').CodefetchConfig} */
export default {
  projectTree: 5,
  tokenLimiter: "truncated",
  defaultPromptFile: "default.md",
  excludeFiles: ["**/*.png"],
  excludeDirs: [
    "test",
    "dist",
    ".taskmaster",
    ".cursor",
    ".clinerules",
    ".gemini",
    "docs",
  ],
};
