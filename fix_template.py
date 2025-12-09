
import os

content = """{% extends 'hms/base.html' %}

{% block title %}Dashboard - HMS{% endblock %}

{% block content %}
<div class="space-y-8">
    <!-- Welcome Header -->
    <div class="flex flex-col md:flex-row justify-between items-end">
        <div>
            <h1 class="text-2xl font-bold text-gray-800">Hello, {{ student.user.first_name }}!</h1>
            <p class="text-gray-500">Plan your meals for today and tomorrow.</p>
        </div>
        <div class="mt-4 md:mt-0 flex flex-col items-end gap-2">
            <span class="bg-indigo-50 text-indigo-700 px-3 py-1 rounded-full text-sm font-medium">
                {{ today|date:"l, d M Y" }}
            </span>
            <a href="https://student.pu.ac.ke/Account/Login?ReturnUrl=%2fFinance%2fPesaflowPayment" target="_blank" class="text-sm text-indigo-600 hover:text-indigo-800 underline">
                University Portal
            </a>
        </div>
    </div>

    {% if is_away_today %}
    <div class="bg-amber-100 border-l-4 border-amber-500 text-amber-700 p-4 rounded shadow-sm">
        <p class="font-bold">You are currently marked as AWAY.</p>
        <p>Meal selection is disabled. Update Away Mode settings to resume meals.</p>
    </div>
    {% endif %}

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

        <!-- Today's Card -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden relative">
            <div class="bg-indigo-600 p-4 flex justify-between items-center text-white">
                <h2 class="font-bold text-lg">Today</h2>
                <span class="text-sm opacity-90">{{ today|date:"M d" }}</span>
            </div>

            <div class="p-6">
                {% if is_locked %}
                <div class="mb-4 bg-amber-50 text-amber-800 text-xs p-2 rounded flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z">
                        </path>
                    </svg>
                    Breakfast selection is locked (past 08:00 AM)
                </div>
                {% endif %}

                <form action="{% url 'hms:confirm_meals' %}" method="post" class="space-y-4">
                    {% csrf_token %}
                    <input type="hidden" name="date" value="{{ today|date:'Y-m-d' }}">

                    <!-- Breakfast -->
                    <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div class="flex items-center">
                            <span
                                class="w-8 h-8 rounded-full bg-orange-100 flex items-center justify-center text-orange-600 mr-3">
                                🍳
                            </span>
                            <div>
                                <h3 class="font-medium text-gray-900">Breakfast</h3>
                                <p class="text-xs text-gray-500">Served 7:00 - 9:00 AM</p>
                            </div>
                        </div>
                        <label class="relative inline-flex items-center cursor-pointer">
                            <input type="checkbox" name="breakfast" class="sr-only peer" {% if meal_today.breakfast %}checked{% endif %} {% if is_locked or is_away_today %}disabled{% endif %}>
                            <div
                                class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-500 {% if is_locked or is_away_today %}opacity-50 cursor-not-allowed{% endif %}">
                            </div>
                        </label>
                    </div>

                    <!-- Early Breakfast Option -->
                    <div class="flex items-center justify-between p-2 pl-14 -mt-2">
                        <span class="text-xs text-gray-500">Need early breakfast? (Before 7am)</span>
                        <input type="checkbox" name="early" class="rounded text-indigo-600 focus:ring-indigo-500" {% if meal_today.early %}checked{% endif %} {% if is_locked or is_away_today %}disabled{% endif %}>
                    </div>

                    <!-- Supper -->
                    <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div class="flex items-center">
                            <span
                                class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 mr-3">
                                🥣
                            </span>
                            <div>
                                <h3 class="font-medium text-gray-900">Supper</h3>
                                <p class="text-xs text-gray-500">Served 6:00 - 8:00 PM</p>
                            </div>
                        </div>
                        <label class="relative inline-flex items-center cursor-pointer">
                            <input type="checkbox" name="supper" class="sr-only peer" {% if meal_today.supper %}checked{% endif %} {% if is_away_today %}disabled{% endif %}>
                            <div
                                class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-500 {% if is_away_today %}opacity-50 cursor-not-allowed{% endif %}">
                            </div>
                        </label>
                    </div>

                    <div class="pt-2">
                        <button type="submit" {% if is_away_today %}disabled{% endif %}
                            class="w-full bg-indigo-600 text-white font-bold py-2 px-4 rounded hover:bg-indigo-700 transition shadow {% if is_away_today %}opacity-50 cursor-not-allowed{% endif %}">
                            Update Today
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Tomorrow's Card -->
        <div
            class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden relative opacity-90 hover:opacity-100 transition">
            <div class="bg-gray-800 p-4 flex justify-between items-center text-white">
                <h2 class="font-bold text-lg">Tomorrow</h2>
                <span class="text-sm opacity-70">{{ tomorrow|date:"M d" }}</span>
            </div>

            <div class="p-6">
                <!-- Similar form for tomorrow, but no lock -->
                <form action="{% url 'hms:confirm_meals' %}" method="post" class="space-y-4">
                    {% csrf_token %}
                    <input type="hidden" name="date" value="{{ tomorrow|date:'Y-m-d' }}">

                    <!-- Breakfast -->
                    <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div class="flex items-center">
                            <span
                                class="w-8 h-8 rounded-full bg-orange-50 flex items-center justify-center text-orange-400 mr-3">
                                🍳
                            </span>
                            <div>
                                <h3 class="font-medium text-gray-900">Breakfast</h3>
                            </div>
                        </div>
                        <label class="relative inline-flex items-center cursor-pointer">
                            <input type="checkbox" name="breakfast" class="sr-only peer" {% if meal_tomorrow.breakfast %}checked{% endif %} {% if is_away_tomorrow %}disabled{% endif %}>
                            <div
                                class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-gray-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-500 {% if is_away_tomorrow %}opacity-50 cursor-not-allowed{% endif %}">
                            </div>
                        </label>
                    </div>

                    <!-- Early Breakfast Option -->
                    <div class="flex items-center justify-between p-2 pl-14 -mt-2">
                        <span class="text-xs text-gray-500">Need early breakfast?</span>
                        <input type="checkbox" name="early" class="rounded text-indigo-600 focus:ring-indigo-500" {% if meal_tomorrow.early %}checked{% endif %} {% if is_away_tomorrow %}disabled{% endif %}>
                    </div>

                    <!-- Supper -->
                    <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div class="flex items-center">
                            <span
                                class="w-8 h-8 rounded-full bg-blue-50 flex items-center justify-center text-blue-400 mr-3">
                                🥣
                            </span>
                            <div>
                                <h3 class="font-medium text-gray-900">Supper</h3>
                            </div>
                        </div>
                        <label class="relative inline-flex items-center cursor-pointer">
                            <input type="checkbox" name="supper" class="sr-only peer" {% if meal_tomorrow.supper %}checked{% endif %} {% if is_away_tomorrow %}disabled{% endif %}>
                            <div
                                class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-gray-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-500 {% if is_away_tomorrow %}opacity-50 cursor-not-allowed{% endif %}">
                            </div>
                        </label>
                    </div>

                    <div class="pt-2">
                        <button type="submit" {% if is_away_tomorrow %}disabled{% endif %}
                            class="w-full bg-gray-800 text-white font-bold py-2 px-4 rounded hover:bg-gray-900 transition shadow {% if is_away_tomorrow %}opacity-50 cursor-not-allowed{% endif %}">
                            Update Tomorrow
                        </button>
                    </div>
                </form>
            </div>
        </div>

    </div>

    <!-- Away Mode Button -->
    <div
        class="bg-indigo-50 border border-indigo-100 rounded-xl p-6 flex flex-col md:flex-row items-center justify-between">
        <div class="mb-4 md:mb-0">
            <h3 class="font-bold text-indigo-900">Going Away?</h3>
            <p class="text-sm text-indigo-700">Mark yourself as away to automatically cancel meals for a specific
                period.</p>
        </div>
        <button onclick="document.getElementById('away-mode-modal').classList.remove('hidden')"
            class="bg-white text-indigo-600 border border-indigo-200 font-bold py-2 px-6 rounded hover:bg-white hover:shadow transition">
            Set Away Mode
        </button>
    </div>

</div>

<!-- Away Mode Modal -->
<div id="away-mode-modal" class="hidden fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
    <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3 text-center">
            <h3 class="text-lg leading-6 font-medium text-gray-900">Set Away Period</h3>
            <div class="mt-2 text-left">
                <form action="{% url 'hms:toggle_away' %}" method="post">
                    {% csrf_token %}
                    <div class="mb-4">
                        <label class="block text-gray-700 text-sm font-bold mb-2" for="start_date">
                            From Date
                        </label>
                        {{ away_form.start_date }}
                    </div>
                    <div class="mb-6">
                        <label class="block text-gray-700 text-sm font-bold mb-2" for="end_date">
                            To Date
                        </label>
                        {{ away_form.end_date }}
                    </div>
                    <div class="flex items-center justify-between">
                        <button type="button" onclick="document.getElementById('away-mode-modal').classList.add('hidden')"
                            class="bg-gray-400 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
                            Cancel
                        </button>
                        <button type="submit"
                            class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
                            Confirm
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

file_path = os.path.join(os.getcwd(), 'hms', 'templates', 'hms', 'student', 'dashboard.html')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully wrote clean template to {file_path}")
