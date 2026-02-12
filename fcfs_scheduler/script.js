// ==========================================
// FCFS Scheduler - JavaScript Implementation
// ==========================================

// Task Class
class Task {
    constructor(taskId, arrivalTime, burstTime) {
        this.taskId = taskId;
        this.arrivalTime = parseInt(arrivalTime);
        this.burstTime = parseInt(burstTime);
        this.startTime = null;
        this.completionTime = null;
        this.vmId = null;
    }

    getWaitingTime() {
        return this.startTime !== null ? this.startTime - this.arrivalTime : 0;
    }

    getTurnaroundTime() {
        return this.completionTime !== null ? this.completionTime - this.arrivalTime : 0;
    }
}

// Virtual Machine Class
class VirtualMachine {
    constructor(vmId) {
        this.vmId = vmId;
        this.availableTime = 0;
        this.taskHistory = [];
        this.totalBusyTime = 0;
    }

    assignTask(task) {
        // Task starts when both VM is available AND task has arrived
        const startTime = Math.max(this.availableTime, task.arrivalTime);
        const completionTime = startTime + task.burstTime;

        task.startTime = startTime;
        task.completionTime = completionTime;
        task.vmId = this.vmId;

        this.availableTime = completionTime;
        this.totalBusyTime += task.burstTime;
        this.taskHistory.push(task);

        return { startTime, completionTime };
    }

    getUtilization(makespan) {
        return makespan > 0 ? (this.totalBusyTime / makespan) * 100 : 0;
    }
}

// FCFS Scheduler Class
class FCFSScheduler {
    constructor(tasks, vms) {
        this.tasks = tasks;
        this.vms = vms;
        this.makespan = 0;
    }

    sortTasksByArrival() {
        this.tasks.sort((a, b) => {
            if (a.arrivalTime === b.arrivalTime) {
                return a.taskId.localeCompare(b.taskId);
            }
            return a.arrivalTime - b.arrivalTime;
        });
    }

    findEarliestAvailableVM() {
        return this.vms.reduce((earliest, current) => 
            current.availableTime < earliest.availableTime ? current : earliest
        );
    }

    simulate() {
        this.sortTasksByArrival();

        // Assign each task to the earliest available VM
        for (const task of this.tasks) {
            const vm = this.findEarliestAvailableVM();
            vm.assignTask(task);
        }

        // Calculate makespan
        this.makespan = Math.max(...this.vms.map(vm => vm.availableTime));
    }

    getMetrics() {
        const totalWaitingTime = this.tasks.reduce((sum, task) => sum + task.getWaitingTime(), 0);
        const totalTurnaroundTime = this.tasks.reduce((sum, task) => sum + task.getTurnaroundTime(), 0);
        const avgUtilization = this.vms.reduce((sum, vm) => sum + vm.getUtilization(this.makespan), 0) / this.vms.length;

        return {
            makespan: this.makespan,
            avgWaitingTime: (totalWaitingTime / this.tasks.length).toFixed(2),
            avgTurnaroundTime: (totalTurnaroundTime / this.tasks.length).toFixed(2),
            avgUtilization: avgUtilization.toFixed(2)
        };
    }
}

// ==========================================
// UI Functions
// ==========================================

function generateTaskInputs() {
    const numVMs = parseInt(document.getElementById('numVMs').value);
    const numTasks = parseInt(document.getElementById('numTasks').value);

    // Validate inputs
    if (numVMs < 2 || numVMs > 3) {
        alert('Number of VMs must be between 2 and 3');
        return;
    }

    if (numTasks < 5 || numTasks > 6) {
        alert('Number of tasks must be between 5 and 6');
        return;
    }

    // Generate task input fields
    const taskInputsContainer = document.getElementById('taskInputs');
    taskInputsContainer.innerHTML = '';

    for (let i = 1; i <= numTasks; i++) {
        const taskCard = document.createElement('div');
        taskCard.className = 'task-input-card';
        taskCard.innerHTML = `
            <h3>Task T${i}</h3>
            <div class="input-group">
                <label>Arrival Time</label>
                <input type="number" id="arrival_${i}" min="0" value="${i - 1}" required>
            </div>
            <div class="input-group">
                <label>Burst Time (CPU Time)</label>
                <input type="number" id="burst_${i}" min="1" value="${Math.floor(Math.random() * 6) + 3}" required>
            </div>
        `;
        taskInputsContainer.appendChild(taskCard);
    }

    // Show task input section
    document.getElementById('taskInputSection').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';

    // Smooth scroll to task inputs
    document.getElementById('taskInputSection').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function loadSampleData() {
    const sampleData = [
        { arrival: 0, burst: 5 },
        { arrival: 1, burst: 8 },
        { arrival: 2, burst: 3 },
        { arrival: 3, burst: 7 },
        { arrival: 4, burst: 4 },
        { arrival: 5, burst: 6 }
    ];

    const numTasks = parseInt(document.getElementById('numTasks').value);
    for (let i = 1; i <= numTasks; i++) {
        document.getElementById(`arrival_${i}`).value = sampleData[i - 1].arrival;
        document.getElementById(`burst_${i}`).value = sampleData[i - 1].burst;
    }
}

function runScheduler() {
    const numVMs = parseInt(document.getElementById('numVMs').value);
    const numTasks = parseInt(document.getElementById('numTasks').value);

    // Collect task data
    const tasks = [];
    for (let i = 1; i <= numTasks; i++) {
        const arrivalTime = document.getElementById(`arrival_${i}`).value;
        const burstTime = document.getElementById(`burst_${i}`).value;

        if (!arrivalTime || !burstTime || burstTime <= 0) {
            alert(`Please fill in valid data for Task T${i}`);
            return;
        }

        tasks.push(new Task(`T${i}`, arrivalTime, burstTime));
    }

    // Create VMs
    const vms = [];
    for (let i = 1; i <= numVMs; i++) {
        vms.push(new VirtualMachine(`VM${i}`));
    }

    // Run scheduler
    const scheduler = new FCFSScheduler(tasks, vms);
    scheduler.simulate();

    // Display results
    displayResults(scheduler);

    // Smooth scroll to results
    setTimeout(() => {
        document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

function displayResults(scheduler) {
    // Show results section
    document.getElementById('resultsSection').style.display = 'block';

    // Display metrics
    displayMetrics(scheduler);

    // Display Gantt chart
    displayGanttChart(scheduler);

    // Display VM utilization
    displayVMUtilization(scheduler);

    // Display execution table
    displayExecutionTable(scheduler);
}

function displayMetrics(scheduler) {
    const metrics = scheduler.getMetrics();

    const metricsHTML = `
        <div class="metric-item">
            <div class="metric-label">Makespan</div>
            <div class="metric-value">${metrics.makespan}</div>
            <div class="metric-label">time units</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Avg Waiting Time</div>
            <div class="metric-value">${metrics.avgWaitingTime}</div>
            <div class="metric-label">time units</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Avg Turnaround Time</div>
            <div class="metric-value">${metrics.avgTurnaroundTime}</div>
            <div class="metric-label">time units</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Avg VM Utilization</div>
            <div class="metric-value">${metrics.avgUtilization}%</div>
            <div class="metric-label">efficiency</div>
        </div>
    `;

    document.getElementById('metricsDisplay').innerHTML = metricsHTML;
}

function displayGanttChart(scheduler) {
    const ganttContainer = document.getElementById('ganttChart');
    const makespan = scheduler.makespan;

    // Task colors
    const taskColors = [
        '#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', 
        '#10b981', '#3b82f6', '#ef4444', '#14b8a6'
    ];

    // Create time axis
    let axisHTML = '<div class="gantt-axis">';
    for (let i = 0; i <= makespan; i++) {
        axisHTML += `<div class="gantt-tick">${i}</div>`;
    }
    axisHTML += '</div>';

    // Create Gantt rows for each VM
    let ganttHTML = axisHTML;

    scheduler.vms.forEach(vm => {
        ganttHTML += `
            <div class="gantt-row">
                <div class="gantt-label">${vm.vmId}</div>
                <div class="gantt-timeline">
        `;

        vm.taskHistory.forEach((task, index) => {
            const leftPercent = (task.startTime / makespan) * 100;
            const widthPercent = (task.burstTime / makespan) * 100;
            const color = taskColors[parseInt(task.taskId.substring(1)) - 1];

            ganttHTML += `
                <div class="gantt-task" 
                     style="left: ${leftPercent}%; width: ${widthPercent}%; background: ${color};"
                     title="${task.taskId}: Start=${task.startTime}, End=${task.completionTime}">
                    ${task.taskId}
                </div>
            `;
        });

        ganttHTML += `
                </div>
            </div>
        `;
    });

    ganttContainer.innerHTML = ganttHTML;
}

function displayVMUtilization(scheduler) {
    const utilizationContainer = document.getElementById('vmUtilization');
    let utilizationHTML = '';

    scheduler.vms.forEach(vm => {
        const utilization = vm.getUtilization(scheduler.makespan);
        let utilizationClass = 'low';
        if (utilization >= 70) utilizationClass = 'high';
        else if (utilization >= 40) utilizationClass = 'medium';

        utilizationHTML += `
            <div class="vm-bar-container">
                <div class="vm-bar-label">
                    <span>${vm.vmId}</span>
                    <span>${utilization.toFixed(2)}% (${vm.totalBusyTime}/${scheduler.makespan} time units)</span>
                </div>
                <div class="vm-bar-background">
                    <div class="vm-bar-fill ${utilizationClass}" style="width: ${utilization}%">
                        ${utilization.toFixed(1)}%
                    </div>
                </div>
            </div>
        `;
    });

    utilizationContainer.innerHTML = utilizationHTML;
}

function displayExecutionTable(scheduler) {
    const tableContainer = document.getElementById('executionTable');

    let tableHTML = `
        <table>
            <thead>
                <tr>
                    <th>Task ID</th>
                    <th>Arrival Time</th>
                    <th>Burst Time</th>
                    <th>Start Time</th>
                    <th>Completion Time</th>
                    <th>VM</th>
                    <th>Waiting Time</th>
                    <th>Turnaround Time</th>
                </tr>
            </thead>
            <tbody>
    `;

    scheduler.tasks.forEach(task => {
        tableHTML += `
            <tr>
                <td><strong>${task.taskId}</strong></td>
                <td>${task.arrivalTime}</td>
                <td>${task.burstTime}</td>
                <td>${task.startTime}</td>
                <td>${task.completionTime}</td>
                <td><strong>${task.vmId}</strong></td>
                <td>${task.getWaitingTime()}</td>
                <td>${task.getTurnaroundTime()}</td>
            </tr>
        `;
    });

    tableHTML += `
            </tbody>
        </table>
    `;

    tableContainer.innerHTML = tableHTML;
}

// ==========================================
// Initialize on page load
// ==========================================

window.addEventListener('DOMContentLoaded', () => {
    console.log('FCFS Cloud Video Rendering Scheduler loaded successfully');
});
