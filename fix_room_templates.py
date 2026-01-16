
import os

# --- Content for hms/templates/hms/admin/room_list.html ---
room_list_content = """{% extends 'hms/base.html' %}

{% block title %}Manage Rooms - HMS{% endblock %}

{% block content %}
<div class="max-w-7xl mx-auto px-4 py-8 space-y-6">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
            <h1 class="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-violet-400 to-purple-300">
                Room Management
            </h1>
            <p class="text-gray-400 mt-2">Manage hostel rooms, availability, and assignments</p>
        </div>
        <a href="{% url 'hms:create_room' %}"
            class="inline-flex items-center justify-center px-6 py-3 bg-gradient-to-r from-violet-500 to-purple-500 hover:from-violet-400 hover:to-purple-400 text-white font-bold rounded-xl shadow-lg transform hover:-translate-y-1 transition duration-200">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Add Room
        </a>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="bg-slate-800/90 backdrop-blur-lg rounded-xl border border-white/10 p-6">
            <div class="flex items-center justify-between">
                <div>
                    <p class="text-gray-400 text-sm">Total Rooms</p>
                    <p class="text-3xl font-bold text-white mt-1">{{ total_rooms }}</p>
                </div>
                <div class="w-12 h-12 rounded-lg bg-violet-500/20 flex items-center justify-center">
                    <svg class="w-6 h-6 text-violet-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                </div>
            </div>
        </div>
        <div class="bg-slate-800/90 backdrop-blur-lg rounded-xl border border-white/10 p-6">
            <div class="flex items-center justify-between">
                <div>
                    <p class="text-gray-400 text-sm">Available</p>
                    <p class="text-3xl font-bold text-emerald-400 mt-1">{{ available_rooms }}</p>
                </div>
                <div class="w-12 h-12 rounded-lg bg-emerald-500/20 flex items-center justify-center">
                    <svg class="w-6 h-6 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                </div>
            </div>
        </div>
        <div class="bg-slate-800/90 backdrop-blur-lg rounded-xl border border-white/10 p-6">
            <div class="flex items-center justify-between">
                <div>
                    <p class="text-gray-400 text-sm">Occupied</p>
                    <p class="text-3xl font-bold text-orange-400 mt-1">{{ occupied_rooms }}</p>
                </div>
                <div class="w-12 h-12 rounded-lg bg-orange-500/20 flex items-center justify-center">
                    <svg class="w-6 h-6 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                </div>
            </div>
        </div>
    </div>

    <!-- Filter Form -->
    <div class="bg-slate-800/90 backdrop-blur-lg rounded-2xl border border-white/10 shadow-xl p-6">
        <form method="get" class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="relative">
                <input type="text" name="block" value="{{ request.GET.block|default:'' }}"
                    class="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all hover:bg-black/30"
                    placeholder="Filter by block...">
            </div>
            <div class="relative">
                <select name="availability"
                    class="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all hover:bg-black/30 appearance-none">
                    <option value="" class="bg-gray-800">All Rooms</option>
                    <option value="available" {% if request.GET.availability == 'available' %}selected{% endif %}
                        class="bg-gray-800">Available Only</option>
                    <option value="occupied" {% if request.GET.availability == 'occupied' %}selected{% endif %}
                        class="bg-gray-800">Occupied Only</option>
                </select>
                <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-gray-400">
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                </div>
            </div>
            <button type="submit"
                class="px-6 py-3 bg-white/10 border border-white/10 text-white font-medium rounded-xl hover:bg-white/20 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-500">
                Apply Filters
            </button>
        </form>
    </div>

    <!-- Rooms Table -->
    {% if rooms %}
    <div class="bg-slate-800/90 backdrop-blur-lg rounded-2xl border border-white/10 shadow-xl overflow-hidden">
        <div class="overflow-x-auto">
            <table class="w-full text-left text-gray-300">
                <thead class="bg-black/20 text-xs uppercase text-gray-400 font-medium tracking-wider">
                    <tr>
                        <th class="px-6 py-4">Room</th>
                        <th class="px-6 py-4">Block / Floor</th>
                        <th class="px-6 py-4">Type</th>
                        <th class="px-6 py-4 text-center">Capacity</th>
                        <th class="px-6 py-4 text-center">Status</th>
                        <th class="px-6 py-4 text-center">Actions</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-white/5">
                    {% for room in rooms %}
                    <tr class="hover:bg-white/5 transition-colors duration-200">
                        <td class="px-6 py-4">
                            <div class="flex items-center gap-3">
                                <div
                                    class="w-10 h-10 rounded-lg bg-gradient-to-br from-violet-500/20 to-purple-500/20 flex items-center justify-center">
                                    <svg class="w-5 h-5 text-violet-400" fill="none" stroke="currentColor"
                                        viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                                    </svg>
                                </div>
                                <span class="font-bold text-white">{{ room.room_number }}</span>
                            </div>
                        </td>
                        <td class="px-6 py-4 text-gray-400">
                            {{ room.block|default:"N/A" }} / Floor {{ room.floor|default:"N/A" }}
                        </td>
                        <td class="px-6 py-4">
                            <span
                                class="px-2 py-1 rounded text-xs font-bold bg-violet-500/20 text-violet-300 border border-violet-500/30">
                                {{ room.get_room_type_display }}
                            </span>
                        </td>
                        <td class="px-6 py-4 text-center">{{ room.capacity }}</td>
                        <td class="px-6 py-4 text-center">
                            {% if room.is_available %}
                            <span
                                class="px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                                Available
                            </span>
                            {% else %}
                            <span
                                class="px-3 py-1 rounded-full text-xs font-bold bg-orange-500/20 text-orange-400 border border-orange-500/30">
                                Occupied
                            </span>
                            {% endif %}
                        </td>
                        <td class="px-6 py-4 text-center">
                            <div class="flex items-center justify-center gap-2">
                                <a href="{% url 'hms:edit_room' room.pk %}"
                                    class="p-2 text-violet-400 hover:text-white hover:bg-violet-500/20 rounded-lg transition"
                                    title="Edit">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                    </svg>
                                </a>
                                <form method="post" action="{% url 'hms:delete_room' room.pk %}" class="inline"
                                    onsubmit="return confirm('Are you sure you want to delete room {{ room.room_number }}?')">
                                    {% csrf_token %}
                                    <button type="submit"
                                        class="p-2 text-red-400 hover:text-white hover:bg-red-500/20 rounded-lg transition"
                                        title="Delete">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                        </svg>
                                    </button>
                                </form>
                            </div>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    {% else %}
    <div class="bg-slate-800/90 backdrop-blur-lg rounded-2xl border border-white/10 shadow-xl p-12 text-center">
        <svg class="w-16 h-16 text-gray-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
        <h3 class="text-xl font-medium text-gray-300">No Rooms Found</h3>
        <p class="text-gray-500 mt-2">Add rooms to start managing hostel accommodations.</p>
        <a href="{% url 'hms:create_room' %}"
            class="inline-flex items-center mt-6 px-6 py-3 bg-gradient-to-r from-violet-500 to-purple-500 text-white font-bold rounded-xl shadow-lg hover:shadow-violet-500/20 transition">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Create First Room
        </a>
    </div>
    {% endif %}

    <!-- Quick Links -->
    <div class="flex flex-wrap gap-3">
        <a href="{% url 'hms:room_assignments' %}"
            class="px-4 py-2 rounded-lg bg-violet-500/20 border border-violet-500/30 text-violet-300 hover:bg-violet-500/30 transition">
            View Assignments
        </a>
        <a href="{% url 'hms:room_change_requests' %}"
            class="px-4 py-2 rounded-lg bg-orange-500/20 border border-orange-500/30 text-orange-300 hover:bg-orange-500/30 transition">
            Change Requests
        </a>
        <a href="{% url 'hms:admin_dashboard' %}"
            class="px-4 py-2 rounded-lg border border-white/20 text-gray-300 hover:bg-white/5 transition">
            ← Back to Dashboard
        </a>
    </div>
</div>
{% endblock %}
"""

# --- Content for hms/templates/hms/admin/room_form.html ---
room_form_content = """{% extends 'hms/base.html' %}

{% block title %}{{ action }} Room - HMS{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto px-4 py-8">
    <div class="bg-slate-800/90 backdrop-blur-lg rounded-2xl border border-white/10 shadow-xl p-8">
        <div class="mb-8">
            <h1 class="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-violet-400 to-purple-300">
                {{ action }} Room
            </h1>
            <p class="text-gray-400 mt-2">{% if action == 'Edit' %}Update room details{% else %}Add a new room to the
                hostel{% endif %}</p>
        </div>

        <form method="post" class="space-y-6">
            {% csrf_token %}

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="space-y-2">
                    <label class="block text-sm font-medium text-gray-300">Room Number</label>
                    <input type="text" name="room_number" value="{{ form.room_number.value|default:'' }}" required
                        class="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all hover:bg-black/30"
                        placeholder="e.g., A-101">
                    {% if form.room_number.errors %}
                    <p class="text-red-400 text-sm">{{ form.room_number.errors.0 }}</p>
                    {% endif %}
                </div>

                <div class="space-y-2">
                    <label class="block text-sm font-medium text-gray-300">Room Type</label>
                    <div class="relative">
                        <select name="room_type" required
                            class="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all hover:bg-black/30 appearance-none">
                            <option value="single" {% if form.room_type.value == 'single' %}selected{% endif %}
                                class="bg-gray-800">Single</option>
                            <option value="double" {% if form.room_type.value == 'double' %}selected{% endif %}
                                class="bg-gray-800">Double</option>
                            <option value="triple" {% if form.room_type.value == 'triple' %}selected{% endif %}
                                class="bg-gray-800">Triple</option>
                            <option value="quad" {% if form.room_type.value == 'quad' %}selected{% endif %}
                                class="bg-gray-800">Quad</option>
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
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="space-y-2">
                    <label class="block text-sm font-medium text-gray-300">Block</label>
                    <input type="text" name="block" value="{{ form.block.value|default:'' }}"
                        class="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all hover:bg-black/30"
                        placeholder="e.g., A, B, C">
                </div>

                <div class="space-y-2">
                    <label class="block text-sm font-medium text-gray-300">Floor</label>
                    <input type="number" name="floor" value="{{ form.floor.value|default:'' }}" min="0"
                        class="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all hover:bg-black/30"
                        placeholder="e.g., 1, 2, 3">
                </div>

                <div class="space-y-2">
                    <label class="block text-sm font-medium text-gray-300">Capacity</label>
                    <input type="number" name="capacity" value="{{ form.capacity.value|default:'1' }}" min="1" max="10"
                        required
                        class="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all hover:bg-black/30"
                        placeholder="Number of beds">
                </div>
            </div>

            <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-300">Monthly Price (KES)</label>
                <input type="number" name="price_per_month" value="{{ form.price_per_month.value|default:'0' }}" min="0"
                    step="0.01"
                    class="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent transition-all hover:bg-black/30"
                    placeholder="e.g., 5000">
            </div>

            <div class="flex items-center pb-1">
                <label
                    class="flex items-center space-x-3 cursor-pointer p-2 rounded-lg hover:bg-white/5 transition duration-200">
                    <div class="relative">
                        <input type="checkbox" name="is_available" class="sr-only peer" {% if form.is_available.value or
                            not room %}checked{% endif %}>
                        <div
                            class="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-violet-500 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-500">
                        </div>
                    </div>
                    <span class="text-gray-300 font-medium select-none">Available for Assignment</span>
                </label>
            </div>

            <div class="flex items-center gap-4 pt-6 border-t border-white/10">
                <button type="submit"
                    class="flex-1 bg-gradient-to-r from-violet-500 to-purple-500 hover:from-violet-400 hover:to-purple-400 text-white font-bold py-3 px-6 rounded-xl shadow-lg transform hover:-translate-y-1 transition duration-200">
                    {{ action }} Room
                </button>
                <a href="{% url 'hms:room_list' %}"
                    class="px-6 py-3 rounded-xl border border-white/20 text-gray-300 hover:bg-white/5 transition text-center min-w-[120px]">
                    Cancel
                </a>
            </div>
        </form>
    </div>
</div>
{% endblock %}
"""

path_list = r"c:\Users\jamal\OneDrive\Desktop\HMS\Hostel-Management-System-HMS-\hms\templates\hms\admin\room_list.html"
path_form = r"c:\Users\jamal\OneDrive\Desktop\HMS\Hostel-Management-System-HMS-\hms\templates\hms\admin\room_form.html"

# Write to file 1
with open(path_list, "w", encoding='utf-8') as f:
    f.write(room_list_content)
print(f"Successfully wrote to {path_list}")

# Write to file 2
with open(path_form, "w", encoding='utf-8') as f:
    f.write(room_form_content)
print(f"Successfully wrote to {path_form}")
