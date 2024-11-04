from gitops_configserver.templates_rendering import (
    VariablesResolver,
    MatrixResolver,
)


def test_variables_resolver():
    template_variables_mapping = [
        {"tenant_variable": "aaa", "tpl_variable": "template.var1"},
        {"tenant_variable": "bbb", "tpl_variable": "template.var2"},
        {"tenant_variable": "ccc", "tpl_variable": "template.var3"},
    ]
    tenant_variables = {
        "aaa": "aaa1.default",
        "bbb": "bbb1.default",
        "ccc": "ccc1.default",
    }
    resolved_variables = VariablesResolver.resolve_for_template(
        template_variables_mapping,
        tenant_variables,
    )
    assert resolved_variables == {
        "template.var1": "aaa1.default",
        "template.var2": "bbb1.default",
        "template.var3": "ccc1.default",
    }


def test_matrix_resolver():
    tenant_variables = {
        "aaa": "aaa1.default",
        "bbb": "bbb1.default",
        "ccc": "ccc1.default",
        "python_version": ["3.11", "3.12"],
    }
    matrix = {
        "os": ["ubuntu-22.04", "ubuntu-20.04"],
        "version": ["10"],
        "python_version": "{{ python_version }}",
    }
    resolved_variants = MatrixResolver.resolve(matrix, tenant_variables)
    assert resolved_variants == [
        {
            "os": "ubuntu-22.04",
            "python_version": "3.11",
            "version": "10",
        },
        {
            "os": "ubuntu-22.04",
            "python_version": "3.12",
            "version": "10",
        },
        {
            "os": "ubuntu-20.04",
            "python_version": "3.11",
            "version": "10",
        },
        {
            "os": "ubuntu-20.04",
            "python_version": "3.12",
            "version": "10",
        },
    ]
