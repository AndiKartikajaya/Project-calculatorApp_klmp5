/**
 * Authentication module for MathHub Calculator
 * Handles user registration, login, and session management
 */

// Global error handler for auth
window.authErrors = [];

class AuthManager {
  constructor() {
    this.baseUrl = "http://localhost:8000/api";
    this.tokenKey = "mathhub_token";
    this.userKey = "mathhub_user";
    this.init();
  }

  init() {
    this.checkAuthState();
    this.bindEvents();
  }

  bindEvents() {
    // Login form
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
      loginForm.addEventListener("submit", (e) => this.handleLogin(e));
    }

    // Register form
    const registerForm = document.getElementById("registerForm");
    if (registerForm) {
      registerForm.addEventListener("submit", (e) => this.handleRegister(e));
    }

    // Logout button
    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
      logoutBtn.addEventListener("click", () => this.logout());
    }
  }

  checkAuthState() {
    const token = this.getToken();
    const currentPage = window.location.href;

    console.log("Current page:", currentPage);
    console.log("Has token:", !!token);

    // Jika di halaman auth tapi sudah login
    if (token && currentPage.includes("auth.html")) {
      console.log("Redirecting to calculator...");
      setTimeout(() => {
        // Gunakan relative path
        window.location.href = "index.html";
      }, 100);
      return;
    }

    // Jika tidak di halaman auth tapi belum login
    if (!token && !currentPage.includes("auth.html")) {
      console.log("Redirecting to auth...");
      setTimeout(() => {
        window.location.href = "auth.html";
      }, 100);
      return;
    }
  }

  getToken() {
    return localStorage.getItem(this.tokenKey);
  }

  getUser() {
    const userStr = localStorage.getItem(this.userKey);
    return userStr ? JSON.parse(userStr) : null;
  }

  setAuthData(token, user) {
    localStorage.setItem(this.tokenKey, token);
    localStorage.setItem(this.userKey, JSON.stringify(user));
  }

  clearAuthData() {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.userKey);
  }

  async handleLogin(e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);
    const username = formData.get("username");
    const password = formData.get("password");

    // Validate
    if (!username || !password) {
      this.showAlert("Please fill in all fields", "error");
      return;
    }

    try {
      this.showLoading(true);

      const response = await fetch(`${this.baseUrl}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Login failed");
      }

      // Save auth data
      this.setAuthData(data.access_token, data.user);

      // Show success message
      this.showAlert("Login successful! Redirecting...", "success");

      // Redirect to calculator
      setTimeout(() => {
        window.location.href = "index.html";
      }, 1500);
    } catch (error) {
      this.showAlert(error.message, "error");
    } finally {
      this.showLoading(false);
    }
  }

  async handleRegister(e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    const userData = {
      username: formData.get("username"),
      email: formData.get("email"),
      password: formData.get("password"),
      confirmPassword: formData.get("confirmPassword"),
    };

    // Validate
    const errors = this.validateRegistration(userData);
    if (errors.length > 0) {
      this.showAlert(errors.join("<br>"), "error");
      return;
    }

    try {
      this.showLoading(true);

      const response = await fetch(`${this.baseUrl}/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: userData.username,
          email: userData.email,
          password: userData.password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Registration failed");
      }

      // Auto login after registration
      const loginResponse = await fetch(`${this.baseUrl}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: userData.username,
          password: userData.password,
        }),
      });

      const loginData = await loginResponse.json();

      if (!loginResponse.ok) {
        throw new Error("Registration successful, but auto-login failed");
      }

      // Save auth data
      this.setAuthData(loginData.access_token, loginData.user);

      // Show success message
      this.showAlert("Registration successful! Redirecting...", "success");

      // Redirect to calculator
      setTimeout(() => {
        window.location.href = "index.html";
      }, 1500);
    } catch (error) {
      this.showAlert(error.message, "error");
    } finally {
      this.showLoading(false);
    }
  }

  validateRegistration(userData) {
    const errors = [];

    if (userData.password.length < 8) {
      errors.push("Password must be at least 8 characters long");
    }

    if (!/\d/.test(userData.password)) {
      errors.push("Password must contain at least one number");
    }

    if (!/[a-zA-Z]/.test(userData.password)) {
      errors.push("Password must contain at least one letter");
    }

    if (userData.password !== userData.confirmPassword) {
      errors.push("Passwords do not match");
    }

    if (!userData.email.includes("@")) {
      errors.push("Please enter a valid email address");
    }

    return errors;
  }

  logout() {
    this.clearAuthData();
    window.location.href = "auth.html";
  }

  showAlert(message, type = "info") {
    // Remove existing alerts
    const existingAlert = document.querySelector(".alert");
    if (existingAlert) {
      existingAlert.remove();
    }

    // Create alert element
    const alertDiv = document.createElement("div");
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `
            <span>${message}</span>
            <button class="close-alert">&times;</button>
        `;

    // Add to page
    const container = document.querySelector(".container") || document.body;
    container.insertBefore(alertDiv, container.firstChild);

    // Add close event
    alertDiv.querySelector(".close-alert").addEventListener("click", () => {
      alertDiv.remove();
    });

    // Auto-remove after 5 seconds
    setTimeout(() => {
      if (alertDiv.parentNode) {
        alertDiv.remove();
      }
    }, 5000);
  }

  showLoading(show) {
    const buttons = document.querySelectorAll('button[type="submit"]');
    buttons.forEach((button) => {
      if (show) {
        button.innerHTML = '<span class="loading"></span> Processing...';
        button.disabled = true;
      } else {
        button.innerHTML = button.dataset.originalText || "Submit";
        button.disabled = false;
      }
    });
  }

  getAuthHeaders() {
    const token = this.getToken();
    return {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    };
  }

  async fetchWithAuth(url, options = {}) {
    const headers = this.getAuthHeaders();
    const response = await fetch(`${this.baseUrl}${url}`, {
      ...options,
      headers: { ...headers, ...options.headers },
    });

    if (response.status === 401) {
      // Token expired or invalid
      this.clearAuthData();
      window.location.href = "auth.html";
      throw new Error("Session expired. Please login again.");
    }

    return response;
  }
}

// Initialize auth manager when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  window.authManager = new AuthManager();
});
