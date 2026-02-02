<?php
/**
 * SEO Machine - Yoast REST API Support
 *
 * Add this code to your theme's functions.php file (or use a code snippets plugin).
 * This enables the SEO Machine tool to set Yoast SEO meta fields via REST API.
 *
 * Fields exposed:
 * - focus_keyphrase (Focus Keyphrase)
 * - seo_title (SEO Title)
 * - meta_description (Meta Description)
 */

add_action('rest_api_init', function() {
    // Only proceed if Yoast SEO is active
    if (!defined('WPSEO_VERSION')) {
        return;
    }

    register_rest_field('post', 'yoast_seo', [
        'get_callback' => function($post) {
            return [
                'focus_keyphrase' => get_post_meta($post['id'], '_yoast_wpseo_focuskw', true),
                'seo_title' => get_post_meta($post['id'], '_yoast_wpseo_title', true),
                'meta_description' => get_post_meta($post['id'], '_yoast_wpseo_metadesc', true),
            ];
        },
        'update_callback' => function($value, $post) {
            if (!current_user_can('edit_post', $post->ID)) {
                return new WP_Error('rest_forbidden', 'Permission denied.', ['status' => 403]);
            }

            if (isset($value['focus_keyphrase'])) {
                update_post_meta($post->ID, '_yoast_wpseo_focuskw', sanitize_text_field($value['focus_keyphrase']));
            }
            if (isset($value['seo_title'])) {
                update_post_meta($post->ID, '_yoast_wpseo_title', sanitize_text_field($value['seo_title']));
            }
            if (isset($value['meta_description'])) {
                update_post_meta($post->ID, '_yoast_wpseo_metadesc', sanitize_text_field($value['meta_description']));
            }

            return true;
        },
        'schema' => [
            'type' => 'object',
            'properties' => [
                'focus_keyphrase' => ['type' => 'string', 'description' => 'Yoast Focus Keyphrase'],
                'seo_title' => ['type' => 'string', 'description' => 'Yoast SEO Title'],
                'meta_description' => ['type' => 'string', 'description' => 'Yoast Meta Description'],
            ],
        ],
    ]);
});
