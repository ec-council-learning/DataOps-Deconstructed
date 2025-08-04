{% macro get_issue_id() %}
    {% set issue_id = env_var('GITHUB_ISSUE_ID', 'no_issue') %}
    {{ return(issue_id) }}
{% endmacro %}

{% macro generate_schema_name(custom_schema_name, node) %}
    {% set issue_id = get_issue_id() %}
    {% if issue_id != 'no_issue' %}
        {{ custom_schema_name | trim }}_issue_{{ issue_id }}
    {% else %}
        {{ custom_schema_name | trim }}
    {% endif %}
{% endmacro %}

{% macro generate_alias_name(custom_alias_name, node) %}
    {% set issue_id = get_issue_id() %}
    {% if issue_id != 'no_issue' %}
        {{ custom_alias_name | trim }}_issue_{{ issue_id }}
    {% else %}
        {{ custom_alias_name | trim }}
    {% endif %}
{% endmacro %}
