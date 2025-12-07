import os

file_path = r'c:\Users\jamal\OneDrive\Desktop\Hostel_System\hms\templates\hms\student\dashboard.html'

content = """{% extends 'hms/base.html' %}

{% block title %}Dashboard - Hostel Meal System{% endblock %}

{% block content %}
<div class="page-header">
    <div class="flex-between">
        <div>
            <h1 class="page-title">Meal Management</h1>
            <p class="page-subtitle">Welcome back, {{ user.first_name }}!</p>
        </div>
        <div>
            <span class="glass-card" style="padding: 0.5rem 1rem; display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.2rem;">🕒</span>
                <span id="live-clock" style="font-weight: 600; font-variant-numeric: tabular-nums;">--:--</span>
            </span>
        </div>
    </div>
</div>

<div class="grid grid-3" style="grid-template-columns: 2fr 1fr;">
    <!-- Main Content -->
    <div class="grid" style="gap: 2rem;">
        <!-- Meal Selection Card -->
        <div class="glass-card" data-tilt>
            <div class="card-header">
                <h3 class="card-title">Today's Meals - {{ today|date:"F d, Y" }}</h3>
                <a href="{% url 'hms:student_profile' %}" class="btn btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.9rem;">
                    View History
                </a>
            </div>
            
            <form method="post" action="{% url 'hms:confirm_meals' %}">
                {% csrf_token %}
                <input type="hidden" name="date" value="{{ today|date:'Y-m-d' }}">
                
                <div class="grid grid-3" style="margin-bottom: 2rem;">
                    <!-- Breakfast -->
                    <div class="glass-card" style="background: rgba(255,255,255,0.02);">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="breakfast" name="breakfast" {% if today_meals.breakfast %}checked{% endif %}>
                            <label class="form-check-label" for="breakfast" style="font-weight: 600;">Breakfast</label>
                        </div>
                        <p class="text-muted" style="font-size: 0.9rem; margin-left: 2rem;">7:00 AM - 9:00 AM</p>
                    </div>

                    <!-- Lunch -->
                    <div class="glass-card" style="background: rgba(255,255,255,0.02);">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="lunch" name="lunch" {% if today_meals.lunch %}checked{% endif %}>
                            <label class="form-check-label" for="lunch" style="font-weight: 600;">Lunch</label>
                        </div>
                        <p class="text-muted" style="font-size: 0.9rem; margin-left: 2rem;">12:30 PM - 2:30 PM</p>
                    </div>

                    <!-- Supper -->
                    <div class="glass-card" style="background: rgba(255,255,255,0.02);">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="supper" name="supper" {% if today_meals.supper %}checked{% endif %}>
                            <label class="form-check-label" for="supper" style="font-weight: 600;">Supper</label>
                        </div>
                        <p class="text-muted" style="font-size: 0.9rem; margin-left: 2rem;">7:30 PM - 9:30 PM</p>
                    </div>
                </div>

                <div class="glass-card" style="background: rgba(99, 102, 241, 0.1); border-color: var(--primary); margin-bottom: 2rem;">
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="early_breakfast" name="early_breakfast" {% if today_meals.early_breakfast_needed %}checked{% endif %}>
                        <label class="form-check-label" for="early_breakfast" style="font-weight: 600; color: var(--primary-light);">
                            Request Early Breakfast (6:00 AM - 7:00 AM)
                        </label>
                    </div>
                    <p class="text-muted" style="font-size: 0.9rem; margin-left: 2rem;">Check this only if you have early morning classes or exams.</p>
                </div>

                <button type="submit" class="btn btn-primary btn-block">
                    <span style="font-size: 1.2rem;">💾</span> Save Meal Preferences
                </button>
            </form>
        </div>

        <!-- Announcements -->
        <div class="glass-card" data-tilt>
            <div class="card-header">
                <h3 class="card-title">Latest Announcements</h3>
            </div>
            {% if announcements %}
                <div class="grid" style="gap: 1rem;">
                {% for announcement in announcements|slice:":3" %}
                    <div style="padding-bottom: 1rem; border-bottom: 1px solid var(--glass-border);">
                        <h5 style="margin-bottom: 0.5rem; color: var(--primary-light);">{{ announcement.title }}</h5>
                        <p class="text-muted" style="font-size: 0.95rem;">{{ announcement.message|truncatewords:30 }}</p>
                        <small style="color: var(--text-secondary); display: block; margin-top: 0.5rem;">
                            🕒 {{ announcement.created_at|timesince }} ago
                        </small>
                    </div>
                {% endfor %}
                </div>
            {% else %}
                <p class="text-muted text-center">No active announcements.</p>
            {% endif %}
        </div>
    </div>

    <!-- Sidebar -->
    <div class="grid" style="gap: 2rem; align-content: start;">
        <!-- Quick Stats -->
        <div class="glass-card" data-tilt>
            <div class="card-header">
                <h3 class="card-title">Quick Stats</h3>
            </div>
            <div class="grid grid-2">
                <div class="stat-card">
                    <div class="stat-value">{{ student.room_number }}</div>
                    <div class="stat-label">Room</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">
                        {% if today_meals.breakfast or today_meals.lunch or today_meals.supper %}
                            <span class="text-success">Active</span>
                        {% else %}
                            <span class="text-muted">None</span>
                        {% endif %}
                    </div>
                    <div class="stat-label">Status</div>
                </div>
            </div>

            <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid var(--glass-border);">
                <h6 class="text-muted" style="margin-bottom: 1rem;">Selected for Today:</h6>
                <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                    {% if today_meals.breakfast %}
                        <span class="btn btn-secondary" style="padding: 0.25rem 0.75rem; font-size: 0.85rem; cursor: default;">Breakfast</span>
                    {% endif %}
                    {% if today_meals.lunch %}
                        <span class="btn btn-secondary" style="padding: 0.25rem 0.75rem; font-size: 0.85rem; cursor: default;">Lunch</span>
                    {% endif %}
                    {% if today_meals.supper %}
                        <span class="btn btn-secondary" style="padding: 0.25rem 0.75rem; font-size: 0.85rem; cursor: default;">Supper</span>
                    {% endif %}
                    {% if not today_meals.breakfast and not today_meals.lunch and not today_meals.supper %}
                        <span class="text-muted" style="font-size: 0.9rem;">No meals selected</span>
                    {% endif %}
                </div>
            </div>
        </div>

        <!-- Away Status -->
        {% if student.is_away %}
        <div class="alert alert-warning">
            <h5 style="color: var(--warning); margin-bottom: 0.5rem;">⚠️ You are marked as Away</h5>
            <p style="font-size: 0.9rem; margin-bottom: 0.5rem;">Until {{ student.away_until|date:"M d, Y" }}</p>
            <a href="{% url 'hms:student_profile' %}" style="font-size: 0.9rem; text-decoration: underline;">Update Status</a>
        </div>
        {% endif %}

        <!-- Upcoming Activities -->
        <div class="glass-card" data-tilt>
            <div class="card-header">
                <h3 class="card-title">Activities</h3>
            </div>
            {% if today_activities %}
                <div class="grid" style="gap: 1rem;">
                {% for activity in today_activities|slice:":3" %}
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h6 style="margin-bottom: 0.2rem;">{{ activity.name }}</h6>
                            <small class="text-muted">{{ activity.get_day_display }}</small>
                        </div>
                        <small class="text-primary" style="font-weight: 500;">
                            {{ activity.start_time|time:"g:i A" }}
                        </small>
                    </div>
                {% endfor %}
                </div>
            {% else %}
                <p class="text-muted text-center">No upcoming activities.</p>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
"""

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully overwrote {file_path}")
