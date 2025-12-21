document.addEventListener('DOMContentLoaded', () => {
  // This script will throw a ReferenceError because the function is not defined.
  console.log("Attempting to call a non-existent function...");
  nonExistentFunction();
});
