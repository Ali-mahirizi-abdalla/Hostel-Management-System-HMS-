
import os

files = {
    r"c:\Users\jamal\OneDrive\Desktop\HMS\Hostel-Management-System-HMS-\hms\templates\hms\admin\announcement_form.html": r"""{% extends 'hms/base.html' %}

{% block title %}{% if edit_mode %}Edit{% else %}Create{% endif %} Announcement - HMS{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto px-4 py-8">
    <div class="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 shadow-xl p-8">
        <div class="mb-8">
            <h1 class="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-teal-400 to-cyan-300">
                {% if edit_mode %}Edit{% else %}Create{% endif %} Announcement
            </h1>
            <p class="text-gray-400 mt-2">Draft a notice to be displayed to all students.</p>
        </div>

        <form method="post" class="space-y-6">
            {% csrf_token %}

            <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-300">Notice Title</label>
                <input type="text" name="title" value="{{ announcement.title|default:'' }}" required
                    class="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all hover:bg-black/30"
                    placeholder="Enter a clear, brief title">
            </div>

            <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-300">Content / Message</label>
                <textarea name="content" rows="8" required
                    class="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all hover:bg-black/30"
                    placeholder="Provide full details of the announcement...">{{ announcement.content|default:'' }}</textarea>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="space-y-2">
                    <label class="block text-sm font-medium text-gray-300">Priority Level</label>
                    <div class="relative">
                        <select name="priority"
                            class="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all hover:bg-black/30 appearance-none">
                            <option value="low" {% if announcement.priority == 'low' %}selected{% endif %}
                                class="bg-gray-800">Low</option>
                            <option value="normal" {% if not announcement.priority or announcement.priority == 'normal' %}selected{% endif %} class="bg-gray-800">Normal</option>
                            <option value="high" {% if announcement.priority == 'high' %}selected{% endif %}
                                class="bg-gray-800">High</option>
                            <option value="urgent" {% if announcement.priority == 'urgent' %}selected{% endif %}
                                class="bg-gray-800">Urgent</option>
                        </select>
                        <div
                            class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-gray-400">
                            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M19 9l-7 7-7-7" />
                            </svg>
                        </div>
                    </div>
                </div>

                <div class="flex items-end pb-1">
                    <label
                        class="flex items-center space-x-3 cursor-pointer p-2 rounded-lg hover:bg-white/5 transition duration-200 w-full md:w-auto">
                        <div class="relative">
                            <input type="checkbox" name="is_active" class="sr-only peer" {% if announcement.is_active or not edit_mode %}checked{% endif %}>
                            <div
                                class="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-teal-500 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-teal-500">
                            </div>
                        </div>
                        <span class="text-gray-300 font-medium select-none">Publish Immediately</span>
                    </label>
                </div>
            </div>

            <div class="flex items-center gap-4 pt-6 border-t border-white/10">
                <button type="submit"
                    class="flex-1 bg-gradient-to-r from-teal-500 to-cyan-500 hover:from-teal-400 hover:to-cyan-400 text-white font-bold py-3 px-6 rounded-xl shadow-lg transform hover:-translate-y-1 transition duration-200">
                    {% if edit_mode %}Update{% else %}Publish{% endif %} Announcement
                </button>
                <a href="{% url 'hms:manage_announcements' %}"
                    class="px-6 py-3 rounded-xl border border-white/20 text-gray-300 hover:bg-white/5 transition text-center min-w-[120px]">
                    Cancel
                </a>
            </div>
        </form>
    </div>
</div>
{% endblock %}""",

    r"c:\Users\jamal\OneDrive\Desktop\HMS\Hostel-Management-System-HMS-\hms\templates\hms\student\meal_history.html": r"""<!-- templates/hms/student/meal_history.html -->
{% extends 'hms/base.html' %}

{% block title %}Meal History - Hostel Meal System{% endblock %}

{% block content %}
<div class="flex justify-between items-center py-4 mb-6 border-b border-slate-200">
    <h1 class="text-2xl font-bold text-slate-800">Meal History</h1>
    <div>
        <a href="{% url 'hms:export_meal_history' %}"
            class="inline-flex items-center px-3 py-2 border border-slate-300 shadow-sm text-sm leading-4 font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
            </svg>
            Export
        </a>
    </div>
</div>

<div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden mb-6">
    <div class="px-6 py-4 border-b border-slate-100 bg-slate-50">
        <h5 class="font-bold text-slate-800">Filter Meals</h5>
    </div>
    <div class="p-6">
        <form method="get" class="grid grid-cols-1 md:grid-cols-12 gap-4">
            <div class="md:col-span-3">
                <label for="start_date" class="block text-sm font-medium text-slate-700 mb-1">From Date</label>
                <input type="date"
                    class="w-full px-3 py-2 bg-white border border-slate-300 rounded text-slate-900 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
                    id="start_date" name="start_date" value="{{ request.GET.start_date }}">
            </div>
            <div class="md:col-span-3">
                <label for="end_date" class="block text-sm font-medium text-slate-700 mb-1">To Date</label>
                <input type="date"
                    class="w-full px-3 py-2 bg-white border border-slate-300 rounded text-slate-900 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
                    id="end_date" name="end_date" value="{{ request.GET.end_date }}">
            </div>
            <div class="md:col-span-4">
                <label for="meal_type" class="block text-sm font-medium text-slate-700 mb-1">Meal Type</label>
                <select
                    class="w-full px-3 py-2 bg-white border border-slate-300 rounded text-slate-900 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
                    id="meal_type" name="meal_type">
                    <option value="">All Meals</option>
                    <option value="breakfast" {% if request.GET.meal_type == 'breakfast' %}selected{% endif %}>Breakfast
                    </option>
                    <option value="lunch" {% if request.GET.meal_type == 'lunch' %}selected{% endif %}>Lunch</option>
                    <option value="dinner" {% if request.GET.meal_type == 'dinner' %}selected{% endif %}>Dinner</option>
                </select>
            </div>
            <div class="md:col-span-2 flex items-end gap-2">
                <button type="submit"
                    class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition shadow-sm">Filter</button>
                <a href="{% url 'hms:meal_history' %}"
                    class="bg-white border border-slate-300 text-slate-700 hover:bg-slate-50 font-bold py-2 px-4 rounded transition shadow-sm">Reset</a>
            </div>
        </form>
    </div>
</div>

<div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
    <div class="p-0 overflow-x-auto">
        <table class="w-full text-left border-collapse">
            <thead>
                <tr
                    class="bg-slate-50 border-b border-slate-100 text-xs font-semibold uppercase tracking-wider text-slate-600">
                    <th class="px-6 py-3">Date</th>
                    <th class="px-6 py-3">Day</th>
                    <th class="px-6 py-3">Breakfast</th>
                    <th class="px-6 py-3">Lunch</th>
                    <th class="px-6 py-3">Dinner</th>
                    <th class="px-6 py-3">Early Breakfast</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 bg-white">
                {% for meal in meal_history %}
                <tr class="hover:bg-slate-50 transition">
                    <td class="px-6 py-4 text-sm text-slate-700">{{ meal.date|date:"M d, Y" }}</td>
                    <td class="px-6 py-4 text-sm text-slate-700">{{ meal.date|date:"l" }}</td>
                    <td class="px-6 py-4 text-sm">
                        {% if meal.breakfast %}
                        <span
                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">Taken</span>
                        {% else %}
                        <span
                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-800">Not
                            Taken</span>
                        {% endif %}
                    </td>
                    <td class="px-6 py-4 text-sm">
                        {% if meal.lunch %}
                        <span
                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">Taken</span>
                        {% else %}
                        <span
                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-800">Not
                            Taken</span>
                        {% endif %}
                    </td>
                    <td class="px-6 py-4 text-sm">
                        {% if meal.dinner %}
                        <span
                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">Taken</span>
                        {% else %}
                        <span
                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-800">Not
                            Taken</span>
                        {% endif %}
                    </td>
                    <td class="px-6 py-4 text-sm">
                        {% if meal.early_breakfast %}
                        <span
                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">Yes</span>
                        {% else %}
                        <span
                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-800">No</span>
                        {% endif %}
                    </td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="6" class="px-6 py-8 text-center text-slate-500 italic">No meal records found</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    {% if is_paginated %}
    <div class="px-6 py-4 border-t border-slate-100">
        <nav aria-label="Page navigation">
            <ul class="flex justify-center space-x-1">
                {% if page_obj.has_previous %}
                <li>
                    <a class="px-3 py-1 border border-slate-300 rounded-md text-slate-600 hover:bg-slate-50"
                        href="?page=1{% if request.GET.start_date %}&start_date={{ request.GET.start_date }}{% endif %}{% if request.GET.end_date %}&end_date={{ request.GET.end_date }}{% endif %}{% if request.GET.meal_type %}&meal_type={{ request.GET.meal_type }}{% endif %}"
                        aria-label="First">
                        <span aria-hidden="true">&laquo;&laquo;</span>
                    </a>
                </li>
                <li>
                    <a class="px-3 py-1 border border-slate-300 rounded-md text-slate-600 hover:bg-slate-50"
                        href="?page={{ page_obj.previous_page_number }}{% if request.GET.start_date %}&start_date={{ request.GET.start_date }}{% endif %}{% if request.GET.end_date %}&end_date={{ request.GET.end_date }}{% endif %}{% if request.GET.meal_type %}&meal_type={{ request.GET.meal_type }}{% endif %}"
                        aria-label="Previous">
                        <span aria-hidden="true">&laquo;</span>
                    </a>
                </li>
                {% endif %}

                {% for num in page_obj.paginator.page_range %}
                {% if page_obj.number == num %}
                <li><span class="px-3 py-1 border border-blue-600 bg-blue-600 text-white rounded-md">{{ num }}</span>
                </li>
                {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %} <li>
                    <a class="px-3 py-1 border border-slate-300 rounded-md text-slate-600 hover:bg-slate-50"
                        href="?page={{ num }}{% if request.GET.start_date %}&start_date={{ request.GET.start_date }}{% endif %}{% if request.GET.end_date %}&end_date={{ request.GET.end_date }}{% endif %}{% if request.GET.meal_type %}&meal_type={{ request.GET.meal_type }}{% endif %}">{{
                        num }}</a>
                    </li>
                    {% endif %}
                    {% endfor %}

                    {% if page_obj.has_next %}
                    <li>
                        <a class="px-3 py-1 border border-slate-300 rounded-md text-slate-600 hover:bg-slate-50"
                            href="?page={{ page_obj.next_page_number }}{% if request.GET.start_date %}&start_date={{ request.GET.start_date }}{% endif %}{% if request.GET.end_date %}&end_date={{ request.GET.end_date }}{% endif %}{% if request.GET.meal_type %}&meal_type={{ request.GET.meal_type }}{% endif %}"
                            aria-label="Next">
                            <span aria-hidden="true">&raquo;</span>
                        </a>
                    </li>
                    <li>
                        <a class="px-3 py-1 border border-slate-300 rounded-md text-slate-600 hover:bg-slate-50"
                            href="?page={{ page_obj.paginator.num_pages }}{% if request.GET.start_date %}&start_date={{ request.GET.start_date }}{% endif %}{% if request.GET.end_date %}&end_date={{ request.GET.end_date }}{% endif %}{% if request.GET.meal_type %}&meal_type={{ request.GET.meal_type }}{% endif %}"
                            aria-label="Last">
                            <span aria-hidden="true">&raquo;&raquo;</span>
                        </a>
                    </li>
                    {% endif %}
            </ul>
        </nav>
    </div>
    {% endif %}
</div>

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
    <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-100 bg-slate-50">
            <h5 class="font-bold text-slate-800">Meal Statistics</h5>
        </div>
        <div class="p-6">
            <div class="grid grid-cols-3 gap-4 text-center">
                <div>
                    <h3 class="text-2xl font-bold text-slate-800">{{ stats.total_breakfast }}</h3>
                    <p class="text-sm text-slate-500">Breakfast</p>
                </div>
                <div>
                    <h3 class="text-2xl font-bold text-slate-800">{{ stats.total_lunch }}</h3>
                    <p class="text-sm text-slate-500">Lunch</p>
                </div>
                <div>
                    <h3 class="text-2xl font-bold text-slate-800">{{ stats.total_dinner }}</h3>
                    <p class="text-sm text-slate-500">Dinner</p>
                </div>
            </div>
        </div>
    </div>
    <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-100 bg-slate-50">
            <h5 class="font-bold text-slate-800">Meal Distribution</h5>
        </div>
        <div class="p-6">
            <div style="height: 200px;">
                <canvas id="mealChart"></canvas>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    // Meal distribution chart
    document.addEventListener('DOMContentLoaded', function () {
        const ctx = document.getElementById('mealChart').getContext('2d');
        const mealChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Breakfast', 'Lunch', 'Dinner'],
                datasets: [{
                    data: [
                        {{ stats.total_breakfast }},
                        {{ stats.total_lunch }},
                        {{ stats.total_dinner }}
                    ],
                    backgroundColor: [
                        'rgba(59, 130, 246, 0.8)',  // Blue
                        'rgba(16, 185, 129, 0.8)', // Emerald
                        'rgba(245, 158, 11, 0.8)'  // Amber
                    ],
                    borderColor: [
                        'rgba(59, 130, 246, 1)',
                        'rgba(16, 185, 129, 1)',
                        'rgba(245, 158, 11, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            padding: 20,
                            font: {
                                family: "'Inter', sans-serif",
                                size: 12
                            }
                        }
                    }
                },
                cutout: '70%',
            }
        });
    });
</script>
{% endblock %}"""
}

for path, content in files.items():
    print(f"Writing to {path}...")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        print("Success.")
    except Exception as e:
        print(f"Error: {e}")
