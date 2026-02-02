<?php
/**
 * Plugin Name: SEO Machine - Yoast REST API Support
 * Description: Exposes Yoast SEO meta fields via the WordPress REST API for the SEO Machine tool.
 * Version: 1.0
 * Author: SEO Machine
 *
 * Installation:
 * 1. Upload this file to: wp-content/mu-plugins/seo-machine-yoast-rest.php
 * 2. That's it - mu-plugins are automatically activated
 *
 * If the mu-plugins folder doesn't exist, create it.
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Register Yoast SEO meta fields for REST API access
 */
add_action('init', function() {
    // Only proceed if Yoast is active
    if (!defined('WPSEO_VERSION')) {
        return;
    }

    $yoast_meta_fields = [
        '_yoast_wpseo_focuskw' => [
            'description' => 'Yoast SEO Focus Keyphrase',
            'single' => true,
        ],
        '_yoast_wpseo_title' => [
            'description' => 'Yoast SEO Title',
            'single' => true,
        ],
        '_yoast_wpseo_metadesc' => [
            'description' => 'Yoast SEO Meta Description',
            'single' => true,
        ],
        '_yoast_wpseo_linkdex' => [
            'description' => 'Yoast SEO Score',
            'single' => true,
        ],
        '_yoast_wpseo_content_score' => [
            'description' => 'Yoast Readability Score',
            'single' => true,
        ],
    ];

    foreach ($yoast_meta_fields as $meta_key => $args) {
        register_post_meta('post', $meta_key, [
            'show_in_rest' => true,
            'single' => $args['single'],
            'type' => 'string',
            'description' => $args['description'],
            'auth_callback' => function() {
                return current_user_can('edit_posts');
            },
        ]);
    }
});

/**
 * Alternative: Add Yoast fields to REST response and handle updates
 * This provides a cleaner API interface
 */
add_action('rest_api_init', function() {
    // Only proceed if Yoast is active
    if (!defined('WPSEO_VERSION')) {
        return;
    }

    // Register a custom field group for Yoast SEO
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
                return new WP_Error('rest_forbidden', 'You do not have permission to edit this post.', ['status' => 403]);
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
                'focus_keyphrase' => ['type' => 'string'],
                'seo_title' => ['type' => 'string'],
                'meta_description' => ['type' => 'string'],
            ],
        ],
    ]);
});
