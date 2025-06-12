// authService.js

let currentUser = null;

export const setUser = (user) => {
  currentUser = user;
};

export const getUser = () => {
  return currentUser;
};

export const clearUser = () => {
  currentUser = null;
};
