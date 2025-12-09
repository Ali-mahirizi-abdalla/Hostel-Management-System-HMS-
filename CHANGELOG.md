# Changelog

All notable changes to the Hostel Management System will be documented in this file.

## [Unreleased] - 2025-12-09

### Added
-   **Django 4.x Upgrade**: migrated project structure and settings.
-   **Tailwind CSS**: Integrated via CDN for responsive, professional UI styling.
-   **Student Profile**:
    -   New `Student` model with `university_id`, `phone`, and `profile_image`.
    -   Profile management view with update capabilities.
-   **Meal Management**:
    -   `Meal` model with boolean flags for Breakfast, Early, Supper, Away.
    -   Time-lock logic: Breakfast selection locks at 8:00 AM.
    -   Dashboard cards for Today and Tomorrow.
-   **Admin/Kitchen Dashboard**:
    -   Aggregated meal counts for today and tomorrow.
    -   CSV Export functionality for meal lists.
-   **Authentication**:
    -   Custom login/registration pages with Tailwind styling.
    -   Password reset flow (templates added).
    -   Automatic profile creation for legacy/admin users to prevent errors.

### Changed
-   **Database**: Configured `dj-database-url` for flexible DB connections (SQLite local, Postgres production).
-   **Static Files**: Configured `whitenoise` for simplified static file serving.
-   **Project Structure**: Cleaned up legacy files and consolidated apps into `hms`.

### Fixed
-   Resolved infinite redirect loop for Staff users and users without profiles.
-   Fixed `datetime` import errors in dashboard views.
