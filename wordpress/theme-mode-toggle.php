<?php
/**
 * Plugin Name: SEO Machine - Theme Mode Toggle
 * Description: Adds a front-end day/night mode toggle with persistent user preference.
 * Version: 1.0
 * Author: SEO Machine
 *
 * Installation (MU-plugin):
 * 1. Upload to: wp-content/mu-plugins/theme-mode-toggle.php
 * 2. Done - mu-plugins auto-activate
 *
 * Alternative:
 * Copy these functions into your active theme's functions.php file.
 */

// Prevent direct access.
if (!defined('ABSPATH')) {
    exit;
}

if (!function_exists('seomachine_theme_mode_styles')) {
    /**
     * Outputs global CSS variables and base styling for light/dark modes.
     */
    function seomachine_theme_mode_styles() {
        if (is_admin()) {
            return;
        }
        ?>
        <style id="seomachine-theme-mode-styles">
            :root {
                color-scheme: light;
                --sm-bg: #f7f8fc;
                --sm-surface: #ffffff;
                --sm-text: #172033;
                --sm-muted: #5b667f;
                --sm-link: #0e5cd6;
                --sm-border: #dbe1ee;
                --sm-shadow: 0 10px 24px rgba(18, 31, 62, 0.08);
                --sm-toggle-bg: #ffffff;
                --sm-toggle-text: #172033;
                --sm-toggle-border: #cfd8ea;
            }

            :root[data-theme="dark"] {
                color-scheme: dark;
                --sm-bg: #111827;
                --sm-surface: #1b2435;
                --sm-text: #e5ecff;
                --sm-muted: #b8c2da;
                --sm-link: #8cb4ff;
                --sm-border: #33415f;
                --sm-shadow: 0 10px 28px rgba(0, 0, 0, 0.45);
                --sm-toggle-bg: #1f2b42;
                --sm-toggle-text: #eaf0ff;
                --sm-toggle-border: #415372;
            }

            html,
            body {
                background-color: var(--sm-bg);
                color: var(--sm-text);
                transition: background-color 0.25s ease, color 0.25s ease;
            }

            a {
                color: var(--sm-link);
            }

            .seomachine-theme-toggle {
                position: fixed;
                right: 20px;
                bottom: 20px;
                z-index: 99999;
                border: 1px solid var(--sm-toggle-border);
                background: var(--sm-toggle-bg);
                color: var(--sm-toggle-text);
                border-radius: 999px;
                padding: 10px 14px;
                font: 600 14px/1.2 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                letter-spacing: 0.01em;
                cursor: pointer;
                box-shadow: var(--sm-shadow);
                transition: transform 0.2s ease, background-color 0.2s ease, color 0.2s ease;
            }

            .seomachine-theme-toggle:hover {
                transform: translateY(-1px);
            }

            .seomachine-theme-toggle:focus-visible {
                outline: 3px solid #4a8fff;
                outline-offset: 2px;
            }

            @media (max-width: 600px) {
                .seomachine-theme-toggle {
                    right: 14px;
                    bottom: 14px;
                    padding: 9px 12px;
                    font-size: 13px;
                }
            }
        </style>
        <?php
    }
}
add_action('wp_head', 'seomachine_theme_mode_styles', 100);

if (!function_exists('seomachine_theme_mode_markup')) {
    /**
     * Adds the front-end mode toggle control.
     */
    function seomachine_theme_mode_markup() {
        if (is_admin()) {
            return;
        }
        ?>
        <button
            type="button"
            class="seomachine-theme-toggle"
            id="seomachine-theme-toggle"
            aria-pressed="false"
            aria-label="Switch to dark mode"
        >
            Night mode
        </button>
        <?php
    }
}
add_action('wp_footer', 'seomachine_theme_mode_markup', 100);

if (!function_exists('seomachine_theme_mode_script')) {
    /**
     * Adds mode persistence and toggle behavior.
     */
    function seomachine_theme_mode_script() {
        if (is_admin()) {
            return;
        }
        ?>
        <script id="seomachine-theme-mode-script">
            (function () {
                var STORAGE_KEY = 'seomachine-theme-mode';
                var root = document.documentElement;
                var button = document.getElementById('seomachine-theme-toggle');
                var mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

                function setButtonState(theme) {
                    if (!button) {
                        return;
                    }
                    var isDark = theme === 'dark';
                    button.textContent = isDark ? 'Day mode' : 'Night mode';
                    button.setAttribute('aria-pressed', String(isDark));
                    button.setAttribute('aria-label', isDark ? 'Switch to day mode' : 'Switch to dark mode');
                }

                function applyTheme(theme, persist) {
                    root.setAttribute('data-theme', theme);
                    setButtonState(theme);
                    if (persist) {
                        try {
                            window.localStorage.setItem(STORAGE_KEY, theme);
                        } catch (error) {
                            // Ignore storage errors (private mode or strict browser settings).
                        }
                    }
                }

                var savedTheme = null;
                try {
                    savedTheme = window.localStorage.getItem(STORAGE_KEY);
                } catch (error) {
                    savedTheme = null;
                }

                if (savedTheme === 'light' || savedTheme === 'dark') {
                    applyTheme(savedTheme, false);
                } else {
                    applyTheme(mediaQuery.matches ? 'dark' : 'light', false);
                }

                if (button) {
                    button.addEventListener('click', function () {
                        var currentTheme = root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
                        var nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
                        applyTheme(nextTheme, true);
                    });
                }

                if (typeof mediaQuery.addEventListener === 'function') {
                    mediaQuery.addEventListener('change', function (event) {
                        var explicitChoice;
                        try {
                            explicitChoice = window.localStorage.getItem(STORAGE_KEY);
                        } catch (error) {
                            explicitChoice = null;
                        }

                        if (explicitChoice !== 'light' && explicitChoice !== 'dark') {
                            applyTheme(event.matches ? 'dark' : 'light', false);
                        }
                    });
                }
            })();
        </script>
        <?php
    }
}
add_action('wp_footer', 'seomachine_theme_mode_script', 101);
