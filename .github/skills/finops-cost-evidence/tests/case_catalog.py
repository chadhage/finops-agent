"""Explicit legacy-test phases; newly added test classes must declare their phase."""

LEGACY_NEGATIVE = {
    "ScopeTests.test_exact_arm_scope_boundary",
    "ScopeTests.test_ambiguous_subscription_name_is_blocked",
    "ScopeTests.test_ambiguous_resource_group_name_is_blocked",
    "ScopeTests.test_ambiguous_directory_identity_is_blocked",
    "ScopeTests.test_ownership_uncertainty_is_not_an_empty_match",
    "ScopeTests.test_stale_business_ownership_is_blocked",
    "ScopeTests.test_management_group_owner_needs_complete_ancestry",
    "ScopeTests.test_unknown_or_empty_filter_is_blocked",
    "ScopeTests.test_tags_are_exact_values_not_fuzzy_or_case_folded",
    "ScopeTests.test_unselected_subscription_and_inventory_are_blocked",
    "ScopeTests.test_missing_inventory_or_mismatched_identity_is_blocked",
    "ScopeTests.test_exact_resource_reference_required_for_scope_validation",
    "ScopeTests.test_partial_day_and_misspelled_basis_are_blocked",
    "PlanTests.test_filter_cannot_be_removed_by_resealing_manifest",
    "PlanTests.test_plan_cannot_contain_non_generated_operations",
    "PlanTests.test_hash_tampering_is_blocked",
    "MoneyAndEvidenceTests.test_duplicate_json_keys_and_nonfinite_numbers_are_blocked",
    "MoneyAndEvidenceTests.test_internal_control_mismatch_is_blocked",
    "MoneyAndEvidenceTests.test_empty_204_is_no_data_not_zero",
    "MoneyAndEvidenceTests.test_missing_query_schema_and_malformed_rows_are_blocked",
    "MoneyAndEvidenceTests.test_cross_scope_and_out_of_period_rows_are_blocked",
    "MoneyAndEvidenceTests.test_unexpected_resource_in_filtered_query_is_blocked",
    "MoneyAndEvidenceTests.test_all_cost_pages_are_required_and_schema_is_stable",
    "MoneyAndEvidenceTests.test_duplicate_paged_rows_and_response_hash_tampering_are_blocked",
    "MoneyAndEvidenceTests.test_reference_compares_per_resource_not_just_total",
    "MoneyAndEvidenceTests.test_exact_reference_match_and_self_reference_rejection",
    "MoneyAndEvidenceTests.test_reference_with_different_cost_basis_is_blocked",
    "MoneyAndEvidenceTests.test_future_or_inconsistent_cost_capture_times_are_blocked",
    "MoneyAndEvidenceTests.test_import_reference_preserves_raw_precision_and_every_page",
    "AzureBoundaryTests.test_app_identity_wrong_tenant_or_wrong_invoker_is_blocked",
    "AzureBoundaryTests.test_continuation_cannot_exfiltrate_token_or_change_scope",
    "AzureBoundaryTests.test_only_read_operations_and_approved_scopes_are_allowed",
    "AzureBoundaryTests.test_403_is_explicit_and_never_zero_cost",
    "AzureBoundaryTests.test_graph_truncation_count_drift_and_duplicate_ids_are_blocked",
    "AzureBoundaryTests.test_inventory_collects_lineage_and_requires_supplied_owner_evidence",
    "AzureBoundaryTests.test_inventory_merges_only_identity_and_scope_bound_ownership",
    "AzureBoundaryTests.test_inventory_does_not_hide_malformed_tags_or_missing_ancestry",
    "ReportingTests.test_no_reference_means_unverified_even_with_correct_internal_totals",
    "ReportingTests.test_both_independent_references_gate_validated_status",
    "ReportingTests.test_html_is_standalone_escaped_and_contains_same_exact_values",
    "ReportingTests.test_markdown_data_cannot_inject_external_images",
    "ReportingTests.test_pdf_failure_is_not_a_success_or_html_fallback",
    "ReportingTests.test_cli_writes_markdown_and_never_overwrites",
    "ReportingTests.test_cli_reconciliation_failure_is_nonzero_and_explicit",
}

LEGACY_POSITIVE = {
    "ScopeTests.test_intersects_categories_and_unions_values",
    "ScopeTests.test_business_owner_is_not_rbac_owner",
    "PlanTests.test_resource_query_and_control_have_identical_filter_and_basis",
    "PlanTests.test_resource_chunks_are_disjoint_and_complete",
    "PlanTests.test_subscription_scope_preserves_unallocated_costs",
    "MoneyAndEvidenceTests.test_raw_numeric_parsing_and_large_sum_are_exact",
    "MoneyAndEvidenceTests.test_sum_is_not_sum_of_rounded_rows",
    "MoneyAndEvidenceTests.test_credits_and_currencies_are_preserved",
    "AzureBoundaryTests.test_identity_is_invoker_bound_without_account_switching",
    "AzureBoundaryTests.test_rate_limit_retry_is_bounded_and_closes_error_response",
    "AzureBoundaryTests.test_graph_pagination_is_complete_and_stable",
    "AzureBoundaryTests.test_execute_preserves_tokens_only_in_client_not_evidence",
    "CustomizationTests.test_discoverable_metadata_and_relative_links",
    "CustomizationTests.test_scenario_example_uses_supported_schema",
}


def phase_for(test_id: str, declared: str | None) -> str:
    if test_id.startswith("test_finops."):
        name = test_id.removeprefix("test_finops.")
        if name in LEGACY_NEGATIVE:
            return "negative"
        if name in LEGACY_POSITIVE:
            return "positive"
    elif declared in ("negative", "positive"):
        return declared
    raise ValueError(f"Unclassified test {test_id}; declare its negative/positive phase explicitly.")
