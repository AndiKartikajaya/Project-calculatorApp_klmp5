/**
 * Calculator module for MathHub Calculator
 * Handles all calculator operations and UI interactions
 */

console.log("Calculator.js loaded");

// Basic Calculator Widget Handler
class BasicCalculator {
  constructor() {
    this.display = document.getElementById("basicDisplay");
    this.resultBox = document.getElementById("basicCalcResult");
    this.exprSpan = document.getElementById("basicCalcExpr");
    this.resultSpan = document.getElementById("basicCalcResultVal");

    console.log("BasicCalculator constructor called");
    console.log("Display element:", this.display);
    console.log("Result box element:", this.resultBox);

    this.currentInput = "0";
    this.operator = null;
    this.previousValue = null;
    this.shouldResetDisplay = false;

    this.init();
  }

  init() {
    console.log("BasicCalculator.init() called");

    // Number buttons
    const numButtons = document.querySelectorAll("[data-number]");
    console.log("Found number buttons:", numButtons.length);
    numButtons.forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        console.log("Number clicked:", e.target.dataset.number);
        this.onNumberClick(e.target.dataset.number);
      });
    });

    // Operator buttons
    const opButtons = document.querySelectorAll("[data-operator]");
    console.log("Found operator buttons:", opButtons.length);
    opButtons.forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        console.log("Operator clicked:", e.target.dataset.operator);
        this.onOperatorClick(e.target.dataset.operator);
      });
    });

    // Action buttons
    const actionButtons = document.querySelectorAll("[data-action]");
    console.log("Found action buttons:", actionButtons.length);
    actionButtons.forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        const action = e.target.dataset.action;
        console.log("Action clicked:", action);
        if (action === "clear") this.clearAll();
        if (action === "delete") this.delete();
        if (action === "equals") this.calculate();
      });
    });

    console.log("BasicCalculator initialization complete");
  }

  onNumberClick(num) {
    if (this.shouldResetDisplay) {
      this.currentInput = num === "." ? "0." : num;
      this.shouldResetDisplay = false;
    } else {
      if (num === ".") {
        if (!this.currentInput.includes(".")) {
          this.currentInput += num;
        }
      } else {
        this.currentInput =
          this.currentInput === "0" ? num : this.currentInput + num;
      }
    }
    this.updateDisplay();
  }

  onOperatorClick(op) {
    if (this.operator !== null && !this.shouldResetDisplay) {
      this.calculate();
    }
    this.previousValue = parseFloat(this.currentInput);
    this.operator = op;
    this.shouldResetDisplay = true;
  }

  calculate() {
    if (this.operator === null) return;

    const currentValue = parseFloat(this.currentInput);
    let result;

    const operatorSymbol =
      this.operator === "*"
        ? "×"
        : this.operator === "/"
          ? "÷"
          : this.operator === "-"
            ? "−"
            : this.operator;

    const expr = `${this.previousValue} ${operatorSymbol} ${currentValue}`;

    switch (this.operator) {
      case "+":
        result = this.previousValue + currentValue;
        break;
      case "-":
        result = this.previousValue - currentValue;
        break;
      case "*":
        result = this.previousValue * currentValue;
        break;
      case "/":
        result = currentValue !== 0 ? this.previousValue / currentValue : 0;
        break;
      case "%":
        result = this.previousValue % currentValue;
        break;
      default:
        return;
    }

    result = Math.round(result * 100000000) / 100000000;

    this.currentInput = String(result);
    this.operator = null;
    this.shouldResetDisplay = true;

    // Tampilkan hanya hasil di display, expression di bawah
    this.display.value = String(result);
    this.showResult(expr, result);
  }

  clearAll() {
    this.currentInput = "0";
    this.operator = null;
    this.previousValue = null;
    this.shouldResetDisplay = false;
    this.resultBox.style.display = "none";
    this.updateDisplay();
  }

  delete() {
    if (this.currentInput.length > 1) {
      this.currentInput = this.currentInput.slice(0, -1);
    } else {
      this.currentInput = "0";
    }
    this.updateDisplay();
  }

  updateDisplay() {
    if (
      this.operator &&
      this.previousValue !== null &&
      !this.shouldResetDisplay
    ) {
      // Tampilkan expression saat operator aktif
      const operatorSymbol =
        this.operator === "*"
          ? "×"
          : this.operator === "/"
            ? "÷"
            : this.operator === "-"
              ? "−"
              : this.operator;
      this.display.value = `${this.previousValue} ${operatorSymbol} ${this.currentInput}`;
    } else if (this.operator && this.previousValue !== null) {
      // Jika baru klik operator, tampilkan operator symbol
      const operatorSymbol =
        this.operator === "*"
          ? "×"
          : this.operator === "/"
            ? "÷"
            : this.operator === "-"
              ? "−"
              : this.operator;
      this.display.value = `${this.previousValue} ${operatorSymbol}`;
    } else {
      // Tampilkan input saat normal
      this.display.value = this.currentInput;
    }
  }

  showResult(expr, result) {
    this.exprSpan.textContent = expr;
    this.resultSpan.textContent = result;
    this.resultBox.style.display = "block";
  }
}

// Export to global scope for easy access
window.BasicCalculator = BasicCalculator;

class Calculator {
  constructor() {
    console.log("Calculator constructor called");

    // Pastikan authManager ada
    if (!window.authManager) {
      console.error("ERROR: authManager is undefined!");
      alert("Authentication system not loaded. Please refresh.");
      return;
    }

    this.authManager = window.authManager;
    // Note: BasicCalculator will be initialized separately via DOMContentLoaded
    this.currentOperation = "basic";
    this.currentBasicOp = "addition";
    this.currentAdvancedOp = "square_root";
    this.currentConversion = { type: "length", from: "meter", to: "kilometer" };
    this.currentFinanceOp = "simple_interest";
    this.angleUnit = "degrees";

    try {
      this.init();
    } catch (error) {
      console.error("Failed to initialize calculator:", error);
      alert("Calculator initialization failed: " + error.message);
    }
  }

  init() {
    console.log("Initializing calculator UI...");
    this.bindEvents();
    this.loadOperations();
    this.updateUI();
    this.updateUserInfo();
  }

  bindEvents() {
    console.log("Binding events...");

    // Navigation
    document.querySelectorAll(".nav-tab").forEach((tab) => {
      tab.addEventListener("click", (e) => this.switchTab(e));
    });

    // Operation selection - akan diisi setelah loadOperations
    // Button events akan di-bind di populateOperationSelectors

    // Calculator form submission
    const basicForm = document.getElementById("basicCalculatorForm");
    if (basicForm) {
      basicForm.addEventListener("submit", (e) => this.calculateBasic(e));
    }

    const advancedForm = document.getElementById("advancedCalculatorForm");
    if (advancedForm) {
      advancedForm.addEventListener("submit", (e) => this.calculateAdvanced(e));
    }

    const conversionForm = document.getElementById("conversionForm");
    if (conversionForm) {
      conversionForm.addEventListener("submit", (e) => this.convertUnits(e));
    }

    const financeForm = document.getElementById("financeForm");
    if (financeForm) {
      financeForm.addEventListener("submit", (e) => this.calculateFinance(e));
    }

    // Angle unit selection
    document.querySelectorAll('input[name="angleUnit"]').forEach((radio) => {
      radio.addEventListener("change", (e) => {
        this.angleUnit = e.target.value;
      });
    });

    // Conversion type selection
    const conversionTypeSelect = document.getElementById("conversionType");
    if (conversionTypeSelect) {
      conversionTypeSelect.addEventListener("change", (e) => {
        this.currentConversion.type = e.target.value;
        this.updateConversionUnits();
      });
    }

    // Clear result button
    const clearBtn = document.getElementById("clearResult");
    if (clearBtn) {
      clearBtn.addEventListener("click", () => this.clearResult());
    }

    // Logout button
    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
      logoutBtn.addEventListener("click", () => {
        this.authManager.logout();
      });
    }
  }

  switchTab(e) {
    e.preventDefault();

    const tab = e.target.closest(".nav-tab");
    if (!tab) return;

    // Update active tab
    document.querySelectorAll(".nav-tab").forEach((t) => {
      t.classList.remove("active");
    });
    tab.classList.add("active");

    // Show corresponding section
    const target = tab.dataset.target;
    document.querySelectorAll(".calculator-section").forEach((section) => {
      section.style.display = "none";
    });

    const targetSection = document.getElementById(`${target}Calculator`);
    if (targetSection) {
      targetSection.style.display = "block";
      this.currentOperation = target;
      this.updateUI();
    }
  }

  async loadOperations() {
    try {
      console.log("Loading operations from API...");
      const response = await fetch(
        `${this.authManager.baseUrl}/calculator/operations`,
      );

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      window.calculatorOperations = data;
      this.populateOperationSelectors(data);
      console.log("Operations loaded successfully");
    } catch (error) {
      console.error("Failed to load operations:", error);
      // Fallback to hardcoded operations
      this.useFallbackOperations();
    }
  }

  useFallbackOperations() {
    console.log("Using fallback operations...");
    window.calculatorOperations = {
      basic_operations: [
        { id: "addition", name: "Addition", symbol: "+", inputs: 2 },
        { id: "subtraction", name: "Subtraction", symbol: "-", inputs: 2 },
        {
          id: "multiplication",
          name: "Multiplication",
          symbol: "×",
          inputs: 2,
        },
        { id: "division", name: "Division", symbol: "÷", inputs: 2 },
        { id: "power", name: "Power", symbol: "^", inputs: 2 },
        { id: "percentage", name: "Percentage", symbol: "%", inputs: 2 },
      ],
      advanced_operations: [
        { id: "square_root", name: "Square Root", symbol: "√", inputs: 1 },
        { id: "sin", name: "Sine", symbol: "sin", inputs: 1 },
        { id: "cos", name: "Cosine", symbol: "cos", inputs: 1 },
        { id: "tan", name: "Tangent", symbol: "tan", inputs: 1 },
        { id: "log", name: "Logarithm", symbol: "log", inputs: 1 },
        { id: "ln", name: "Natural Log", symbol: "ln", inputs: 1 },
      ],
      conversions: {
        length: [
          "meter",
          "kilometer",
          "centimeter",
          "millimeter",
          "mile",
          "yard",
          "foot",
          "inch",
        ],
        weight: ["kilogram", "gram", "pound", "ounce", "ton"],
        temperature: ["celsius", "fahrenheit", "kelvin"],
      },
      finance_operations: [
        { id: "simple_interest", name: "Simple Interest", inputs: 3 },
        { id: "compound_interest", name: "Compound Interest", inputs: 3 },
        { id: "loan_payment", name: "Loan Payment", inputs: 3 },
      ],
    };

    this.populateOperationSelectors(window.calculatorOperations);
  }

  populateOperationSelectors(operations) {
    console.log("Populating operation selectors...");

    // Basic operations
    const basicContainer = document.querySelector(
      '.operation-selector[data-type="basic"]',
    );
    if (basicContainer && operations.basic_operations) {
      basicContainer.innerHTML = operations.basic_operations
        .map(
          (op) => `
                <button type="button" class="operation-btn ${op.id === this.currentBasicOp ? "active" : ""}" 
                        data-operation="${op.id}" data-type="basic">
                    ${op.symbol}<br><small>${op.name}</small>
                </button>
            `,
        )
        .join("");

      // Rebind events
      basicContainer.querySelectorAll(".operation-btn").forEach((btn) => {
        btn.addEventListener("click", (e) => this.selectOperation(e));
      });
    }

    // Advanced operations
    const advancedContainer = document.querySelector(
      '.operation-selector[data-type="advanced"]',
    );
    if (advancedContainer && operations.advanced_operations) {
      advancedContainer.innerHTML = operations.advanced_operations
        .map(
          (op) => `
                <button type="button" class="operation-btn ${op.id === this.currentAdvancedOp ? "active" : ""}" 
                        data-operation="${op.id}" data-type="advanced">
                    ${op.symbol}<br><small>${op.name}</small>
                </button>
            `,
        )
        .join("");

      // Rebind events
      advancedContainer.querySelectorAll(".operation-btn").forEach((btn) => {
        btn.addEventListener("click", (e) => this.selectOperation(e));
      });
    }

    // Conversion types
    const conversionTypeSelect = document.getElementById("conversionType");
    if (conversionTypeSelect && operations.conversions) {
      conversionTypeSelect.innerHTML = Object.keys(operations.conversions)
        .map(
          (type) => `
                <option value="${type}">${type.charAt(0).toUpperCase() + type.slice(1)}</option>
            `,
        )
        .join("");

      // Populate unit selectors
      this.updateConversionUnits();
    }

    // Finance operations
    const financeSelect = document.getElementById("financeOperation");
    if (financeSelect && operations.finance_operations) {
      financeSelect.innerHTML = operations.finance_operations
        .map(
          (op) => `
                <option value="${op.id}">${op.name}</option>
            `,
        )
        .join("");
    }
  }

  updateConversionUnits() {
    if (
      !window.calculatorOperations ||
      !window.calculatorOperations.conversions
    )
      return;

    const conversions = window.calculatorOperations.conversions;
    const type = this.currentConversion.type;
    const units = conversions[type] || [];

    const fromSelect = document.getElementById("fromUnit");
    const toSelect = document.getElementById("toUnit");

    if (fromSelect && toSelect) {
      fromSelect.innerHTML = units
        .map(
          (unit) => `
                <option value="${unit}" ${unit === this.currentConversion.from ? "selected" : ""}>
                    ${unit}
                </option>
            `,
        )
        .join("");

      toSelect.innerHTML = units
        .map(
          (unit) => `
                <option value="${unit}" ${unit === this.currentConversion.to ? "selected" : ""}>
                    ${unit}
                </option>
            `,
        )
        .join("");
    }
  }

  selectOperation(e) {
    const btn = e.target.closest(".operation-btn");
    if (!btn) return;

    const type = btn.dataset.type;
    const operation = btn.dataset.operation;

    // Update active button
    btn
      .closest(".operation-selector")
      .querySelectorAll(".operation-btn")
      .forEach((b) => {
        b.classList.remove("active");
      });
    btn.classList.add("active");

    // Update current operation
    if (type === "basic") {
      this.currentBasicOp = operation;
      this.updateBasicInputs();
    } else if (type === "advanced") {
      this.currentAdvancedOp = operation;
      this.updateAdvancedInputs();
    }
  }

  updateBasicInputs() {
    const operation = window.calculatorOperations?.basic_operations?.find(
      (op) => op.id === this.currentBasicOp,
    );

    if (operation) {
      const num2Group = document.getElementById("num2Group");
      if (num2Group) {
        num2Group.style.display = operation.inputs === 2 ? "block" : "none";
      }
    }
  }

  updateAdvancedInputs() {
    const operation = window.calculatorOperations?.advanced_operations?.find(
      (op) => op.id === this.currentAdvancedOp,
    );

    if (operation) {
      const angleUnitGroup = document.getElementById("angleUnitGroup");
      if (angleUnitGroup) {
        const isTrig = ["sin", "cos", "tan"].includes(this.currentAdvancedOp);
        angleUnitGroup.style.display = isTrig ? "block" : "none";
      }
    }
  }

  updateUI() {
    this.updateBasicInputs();
    this.updateAdvancedInputs();
  }

  async calculateBasic(e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    const num1 = parseFloat(formData.get("num1"));
    const num2 = parseFloat(formData.get("num2"));

    // Validation
    if (isNaN(num1)) {
      this.authManager.showAlert("Please enter a valid first number", "error");
      return;
    }

    const operation = window.calculatorOperations?.basic_operations?.find(
      (op) => op.id === this.currentBasicOp,
    );

    if (operation && operation.inputs === 2 && isNaN(num2)) {
      this.authManager.showAlert("Please enter a valid second number", "error");
      return;
    }

    if (this.currentBasicOp === "division" && num2 === 0) {
      this.authManager.showAlert("Cannot divide by zero", "error");
      return;
    }

    try {
      this.showLoading(true);

      const response = await this.authManager.fetchWithAuth(
        "/calculator/basic",
        {
          method: "POST",
          body: JSON.stringify({
            num1,
            num2: operation.inputs === 2 ? num2 : 0,
            operation: this.currentBasicOp,
          }),
        },
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Calculation failed");
      }

      this.displayResult(data);
      this.authManager.showAlert("Calculation saved to history", "success");
    } catch (error) {
      this.authManager.showAlert(error.message, "error");
    } finally {
      this.showLoading(false);
    }
  }

  async calculateAdvanced(e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    const value = parseFloat(formData.get("value"));

    // Skip validation - silently ignore invalid input
    if (isNaN(value)) {
      return;
    }

    try {
      this.showLoading(true);

      const response = await this.authManager.fetchWithAuth(
        "/calculator/advanced",
        {
          method: "POST",
          body: JSON.stringify({
            value,
            operation: this.currentAdvancedOp,
            angle_unit: this.angleUnit,
          }),
        },
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Calculation failed");
      }

      this.displayResult(data);
      this.authManager.showAlert("Calculation saved to history", "success");
    } catch (error) {
      this.authManager.showAlert(error.message, "error");
    } finally {
      this.showLoading(false);
    }
  }

  async convertUnits(e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    const value = parseFloat(formData.get("value"));
    const fromUnit = formData.get("fromUnit");
    const toUnit = formData.get("toUnit");
    const conversionType = formData.get("conversionType");

    // Skip validation - silently ignore invalid input
    if (isNaN(value)) {
      return;
    }

    if (fromUnit === toUnit) {
      return;
    }

    try {
      this.showLoading(true);

      const response = await this.authManager.fetchWithAuth(
        "/calculator/convert",
        {
          method: "POST",
          body: JSON.stringify({
            value,
            from_unit: fromUnit,
            to_unit: toUnit,
            conversion_type: conversionType,
          }),
        },
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Conversion failed");
      }

      this.displayResult({
        result: data.converted_value,
        expression: `${value} ${fromUnit} = ${data.converted_value}`,
      });

      this.authManager.showAlert("Conversion saved to history", "success");
    } catch (error) {
      this.authManager.showAlert(error.message, "error");
    } finally {
      this.showLoading(false);
    }
  }

  async calculateFinance(e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    const principal = parseFloat(formData.get("principal"));
    const rate = parseFloat(formData.get("rate"));
    const time = parseFloat(formData.get("time"));
    const operation = formData.get("operation");

    // Skip validation - silently ignore invalid input
    if (isNaN(principal) || principal <= 0) {
      return;
    }

    if (isNaN(rate) || rate < 0) {
      return;
    }

    if (isNaN(time) || time <= 0) {
      return;
    }

    try {
      this.showLoading(true);

      const response = await this.authManager.fetchWithAuth(
        "/calculator/finance",
        {
          method: "POST",
          body: JSON.stringify({
            principal,
            rate,
            time,
            operation,
          }),
        },
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Financial calculation failed");
      }

      this.displayResult(data);
      this.authManager.showAlert("Calculation saved to history", "success");
    } catch (error) {
      this.authManager.showAlert(error.message, "error");
    } finally {
      this.showLoading(false);
    }
  }

  displayResult(data) {
    const resultContainer = document.getElementById("resultContainer");
    const resultExpression = document.getElementById("resultExpression");
    const resultValue = document.getElementById("resultValue");

    if (resultContainer && resultExpression && resultValue) {
      resultExpression.textContent = data.expression || "Result";
      resultValue.textContent = data.result || data.converted_value || "N/A";
      resultContainer.style.display = "block";
    }
  }

  clearResult() {
    const resultContainer = document.getElementById("resultContainer");
    if (resultContainer) {
      resultContainer.style.display = "none";
    }

    // Clear form inputs
    document.querySelectorAll("form").forEach((form) => {
      form.reset();
    });
  }

  showLoading(show) {
    const buttons = document.querySelectorAll('form button[type="submit"]');
    buttons.forEach((button) => {
      if (show) {
        button.dataset.originalText = button.textContent;
        button.innerHTML = '<span class="loading"></span> Calculating...';
        button.disabled = true;
      } else {
        button.innerHTML = button.dataset.originalText || "Calculate";
        button.disabled = false;
      }
    });
  }

  updateUserInfo() {
    const user = this.authManager.getUser();
    if (user) {
      const usernameSpan = document.getElementById("usernameDisplay");
      if (usernameSpan) {
        usernameSpan.textContent = user.username;
        console.log("Updated username display:", user.username);
      }
    }
  }
}

console.log("Calculator class defined");

// Export to global scope for easy access
window.BasicCalculator = BasicCalculator;
window.Calculator = Calculator;
console.log("✓ Classes exported to window:", {
  BasicCalculator: window.BasicCalculator,
  Calculator: window.Calculator,
});
