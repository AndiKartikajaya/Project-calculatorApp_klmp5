/**
 * History module for MathHub Calculator
 * Handles calculation history display and management
 */

class HistoryManager {
    constructor() {
        this.authManager = window.authManager;
        this.currentFilters = {
            operation_type: '',
            start_date: '',
            end_date: '',
            limit: 50
        };
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadHistory();
        this.loadStats();
        this.updateUserInfo();
    }

    bindEvents() {
        // Filter form
        const filterForm = document.getElementById('historyFilterForm');
        if (filterForm) {
            filterForm.addEventListener('submit', (e) => this.handleFilter(e));
        }

        // Clear filters button
        const clearFiltersBtn = document.getElementById('clearFilters');
        if (clearFiltersBtn) {
            clearFiltersBtn.addEventListener('click', () => this.clearFilters());
        }

        // Delete actions
        const deleteAllBtn = document.getElementById('deleteAllHistory');
        if (deleteAllBtn) {
            deleteAllBtn.addEventListener('click', () => this.deleteAllHistory());
        }

        // Export buttons
        const exportCSVBtn = document.getElementById('exportCSV');
        if (exportCSVBtn) {
            exportCSVBtn.addEventListener('click', () => this.exportToCSV());
        }

        // Individual delete buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('delete-history-btn')) {
                const historyId = e.target.dataset.id;
                if (historyId) {
                    this.deleteHistory(parseInt(historyId));
                }
            }
        });
    }

    async loadHistory() {
        try {
            this.showLoading(true);
            
            // Build query string from filters
            const queryParams = new URLSearchParams();
            if (this.currentFilters.operation_type) {
                queryParams.append('operation_type', this.currentFilters.operation_type);
            }
            if (this.currentFilters.start_date) {
                queryParams.append('start_date', this.currentFilters.start_date);
            }
            if (this.currentFilters.end_date) {
                queryParams.append('end_date', this.currentFilters.end_date);
            }
            queryParams.append('limit', this.currentFilters.limit);
            
            const response = await this.authManager.fetchWithAuth(`/history/?${queryParams.toString()}`);
            const history = await response.json();

            if (!response.ok) {
                throw new Error('Failed to load history');
            }

            this.displayHistory(history);

        } catch (error) {
            this.authManager.showAlert(error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async loadStats() {
        try {
            const response = await this.authManager.fetchWithAuth('/history/stats');
            const stats = await response.json();

            if (!response.ok) {
                throw new Error('Failed to load statistics');
            }

            this.displayStats(stats);

        } catch (error) {
            console.error('Failed to load stats:', error);
        }
    }

    displayHistory(history) {
        const historyList = document.getElementById('historyList');
        if (!historyList) return;

        if (history.length === 0) {
            historyList.innerHTML = `
                <div class="history-item">
                    <div class="history-info">
                        <p>No calculation history found.</p>
                    </div>
                </div>
            `;
            return;
        }

        historyList.innerHTML = history.map(item => {
            const date = new Date(item.created_at);
            const formattedDate = date.toLocaleDateString();
            const formattedTime = date.toLocaleTimeString();
            
            return `
                <div class="history-item" data-id="${item.id}">
                    <div class="history-info">
                        <span class="history-operation">${this.formatOperationType(item.operation_type)}</span>
                        <p class="history-expression">${item.expression}</p>
                        <p class="history-result">= ${item.result}</p>
                        <p class="history-time">${formattedDate} at ${formattedTime}</p>
                    </div>
                    <div class="history-actions">
                        <button class="btn btn-secondary" onclick="historyManager.copyExpression('${item.expression}')">
                            Copy
                        </button>
                        <button class="btn btn-danger delete-history-btn" data-id="${item.id}">
                            Delete
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    }

    displayStats(stats) {
        // Total calculations
        const totalEl = document.getElementById('totalCalculations');
        if (totalEl) {
            totalEl.textContent = stats.total_calculations || 0;
        }

        // Recent activity
        const recentEl = document.getElementById('recentActivity');
        if (recentEl) {
            recentEl.textContent = stats.recent_activity_count || 0;
        }

        // Operation breakdown
        const breakdownEl = document.getElementById('operationBreakdown');
        if (breakdownEl && stats.operation_counts) {
            const breakdown = Object.entries(stats.operation_counts)
                .map(([op, count]) => `${this.formatOperationType(op)}: ${count}`)
                .join(', ');
            breakdownEl.textContent = breakdown;
        }
    }

    formatOperationType(type) {
        const typeMap = {
            'addition': 'Addition',
            'subtraction': 'Subtraction',
            'multiplication': 'Multiplication',
            'division': 'Division',
            'power': 'Power',
            'square_root': 'Square Root',
            'percentage': 'Percentage',
            'sin': 'Sine',
            'cos': 'Cosine',
            'tan': 'Tangent',
            'log': 'Logarithm',
            'ln': 'Natural Log',
            'conversion': 'Conversion',
            'finance': 'Finance'
        };
        
        return typeMap[type] || type;
    }

    async handleFilter(e) {
        e.preventDefault();
        
        const form = e.target;
        const formData = new FormData(form);
        
        // Update filters
        this.currentFilters = {
            operation_type: formData.get('operation_type') || '',
            start_date: formData.get('start_date') || '',
            end_date: formData.get('end_date') || '',
            limit: parseInt(formData.get('limit')) || 50
        };
        
        // Reload history with new filters
        await this.loadHistory();
        
        this.authManager.showAlert('Filters applied', 'success');
    }

    clearFilters() {
        // Reset filter form
        const form = document.getElementById('historyFilterForm');
        if (form) {
            form.reset();
        }
        
        // Reset filters
        this.currentFilters = {
            operation_type: '',
            start_date: '',
            end_date: '',
            limit: 50
        };
        
        // Reload history
        this.loadHistory();
        
        this.authManager.showAlert('Filters cleared', 'success');
    }

    async deleteHistory(historyId) {
        if (!confirm('Are you sure you want to delete this history record?')) {
            return;
        }

        try {
            const response = await this.authManager.fetchWithAuth(`/history/${historyId}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('Failed to delete history record');
            }

            // Remove from UI
            const item = document.querySelector(`.history-item[data-id="${historyId}"]`);
            if (item) {
                item.remove();
            }
            
            this.authManager.showAlert('History record deleted', 'success');
            
            // Reload stats
            await this.loadStats();

        } catch (error) {
            this.authManager.showAlert(error.message, 'error');
        }
    }

    async deleteAllHistory() {
        if (!confirm('Are you sure you want to delete ALL your calculation history? This action cannot be undone.')) {
            return;
        }

        try {
            const response = await this.authManager.fetchWithAuth('/history/', {
                method: 'DELETE',
                body: JSON.stringify({
                    delete_all: true
                })
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.detail || 'Failed to delete history');
            }

            this.authManager.showAlert(result.message || 'All history deleted', 'success');
            
            // Reload history and stats
            await this.loadHistory();
            await this.loadStats();

        } catch (error) {
            this.authManager.showAlert(error.message, 'error');
        }
    }

    async exportToCSV() {
        try {
            // Build query string from filters
            const queryParams = new URLSearchParams();
            if (this.currentFilters.operation_type) {
                queryParams.append('operation_type', this.currentFilters.operation_type);
            }
            if (this.currentFilters.start_date) {
                queryParams.append('start_date', this.currentFilters.start_date);
            }
            if (this.currentFilters.end_date) {
                queryParams.append('end_date', this.currentFilters.end_date);
            }
            queryParams.append('limit', this.currentFilters.limit);
            
            const response = await this.authManager.fetchWithAuth(`/history/export/csv?${queryParams.toString()}`);
            
            if (!response.ok) {
                throw new Error('Failed to export history');
            }
            
            // Download CSV file
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `calculation_history_${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            this.authManager.showAlert('History exported to CSV', 'success');
            
        } catch (error) {
            this.authManager.showAlert(error.message, 'error');
        }
    }

    copyExpression(expression) {
        navigator.clipboard.writeText(expression)
            .then(() => {
                this.authManager.showAlert('Expression copied to clipboard', 'success');
            })
            .catch(err => {
                console.error('Failed to copy: ', err);
                this.authManager.showAlert('Failed to copy expression', 'error');
            });
    }

    showLoading(show) {
        const historyList = document.getElementById('historyList');
        if (historyList) {
            if (show) {
                historyList.innerHTML = `
                    <div class="history-item">
                        <div class="history-info" style="text-align: center;">
                            <div class="loading" style="margin: 20px auto;"></div>
                            <p>Loading history...</p>
                        </div>
                    </div>
                `;
            }
        }
    }

    updateUserInfo() {
        const user = this.authManager.getUser();
        if (user) {
            const usernameSpan = document.getElementById('usernameDisplay');
            if (usernameSpan) {
                usernameSpan.textContent = user.username;
            }
        }
    }
}

// Initialize history manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (window.authManager && window.authManager.getToken()) {
        window.historyManager = new HistoryManager();
    }
});