
import os

file_path = r"c:\Users\jamal\OneDrive\Desktop\HMS\Hostel-Management-System-HMS-\hms\templates\hms\admin\announcement_form.html"

new_content = """{% extends 'hms/base.html' %}

{% block title %}{% if edit_mode %}Edit{% else %}Create{% endif %} Announcement - HMS{% endblock %}

{% block content %}
<div class="container animate-fade-in">
    <div class="page-header">
        <h1 class="page-title">{% if edit_mode %}Edit{% else %}Create{% endif %} Announcement</h1>
        <p class="page-subtitle">Draft a notice to be displayed to all students.</p>
    </div>

    <div class="glass-card" style="max-width: 800px; margin: 0 auto;">
        <form method="post">
            {% csrf_token %}

            <div class="form-group mb-4">
                <label class="form-label">Notice Title</label>
                <input type="text" name="title" class="form-input" value="{{ announcement.title|default:'' }}" required
                    placeholder="Enter a clear, brief title">
            </div>

            <div class="form-group mb-4">
                <label class="form-label">Content / Message</label>
                <textarea name="content" class="form-textarea" rows="8" required
                    placeholder="Provide full details of the announcement...">{{ announcement.content|default:'' }}</textarea>
            </div>

            <div class="grid grid-2 gap-4">
                <div class="form-group mb-4">
                    <label class="form-label">Priority Level</label>
                    <select name="priority" class="form-select">
                        <option value="low" {% if announcement.priority == 'low' %}selected{% endif %}>Low</option>
                        <option value="normal" {% if not announcement.priority or announcement.priority == 'normal' %}selected{% endif %}>Normal</option>
                        <option value="high" {% if announcement.priority == 'high' %}selected{% endif %}>High</option>
                        <option value="urgent" {% if announcement.priority == 'urgent' %}selected{% endif %}>Urgent</option>
                    </select>
                </div>

                <div class="form-group mb-4 flex items-center" style="padding-top: 1.5rem;">
                    <label class="form-check">
                        <input type="checkbox" name="is_active" class="form-check-input" {% if announcement.is_active or not edit_mode %}checked{% endif %}>
                        <span class="text-secondary font-medium">Publish Immediately</span>
                    </label>
                </div>
            </div>

            <div class="mt-4 flex gap-3">
                <button type="submit" class="btn btn-primary flex-grow">
                    <i class="fas fa-save"></i> {% if edit_mode %}Update{% else %}Publish{% endif %} Announcement
                </button>
                <a href="{% url 'hms:manage_announcements' %}" class="btn btn-secondary">
                    Cancel
                </a>
            </div>
        </form>
    </div>
</div>
{% endblock %}"""

with open(file_path, "w", encoding='utf-8') as f:
    f.write(new_content)

print(f"File {file_path} rewritten successfully.")
