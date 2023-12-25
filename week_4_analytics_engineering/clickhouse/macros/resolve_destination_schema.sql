{% macro resolve_schema_for(model_type) -%}

    {{- resolve_env_prefix() -}} {{- resolve_type(model_type) -}}

{%- endmacro %}


{% macro resolve_env_prefix() -%}

    {%- if target.name != 'prod' -%} {{ 'tmp_' }}
    {%- endif -%}

{%- endmacro %}


{% macro resolve_type(model_type='staging') -%}

    {%- set target_env_var = 'DBT_CLICKHOUSE_TARGET_DATABASE'  -%}
    {%- set stging_env_var = 'DBT_CLICKHOUSE_STAGING_DATABASE' -%}

    {%- if model_type == 'core' -%} {{- env_var(target_env_var) -}}
    {%- else -%}                    {{- env_var(stging_env_var, 'stg_' ~ env_var(target_env_var)) -}}
    {%- endif -%}

{%- endmacro %}
