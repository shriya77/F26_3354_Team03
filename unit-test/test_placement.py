"""
Automated unit tests for the Placement unit (Section 4 of the Final Report).

Run with:  python -m pytest -v

Each test name starts with its test case ID from the Section 4.3 table.
"""

from datetime import date

import pytest

from placement import Placement, PlacementError


def make_history_with_current():
    """A child with one open placement that started on 01/15/2026."""
    history = []
    Placement.add_placement(
        history, 1, "Rivera Family", "Foster family home (non-relative)", date(2026, 1, 15)
    )
    return history


# TC-1 (FR04): A valid first placement is saved and shown as current.
def test_tc1_add_first_placement_is_saved_as_current():
    history = []
    placement = Placement.add_placement(
        history, 1, "Rivera Family", "Foster family home (non-relative)", date(2026, 1, 15)
    )
    assert history == [placement]
    assert placement.is_current
    assert Placement.get_current(history) is placement


# TC-2 (FR04): A placement with no start date is rejected and nothing that is saved.
def test_tc2_missing_start_date_is_rejected():
    history = []
    with pytest.raises(PlacementError, match="Start date is required"):
        Placement.add_placement(history, 1, "Rivera Family", "Group home", None)
    assert history == []


# TC-3 (NFR13): A placement type outside the AFCARS settings that is rejected.
def test_tc3_non_afcars_placement_type_is_rejected():
    history = []
    with pytest.raises(PlacementError, match="not an AFCARS placement setting"):
        Placement.add_placement(history, 1, "Hotel stay", "Hotel", date(2026, 1, 15))
    assert history == []


# TC-4 (FR05): A valid end date closes the placement and moves it to history.
def test_tc4_valid_end_date_closes_placement():
    history = make_history_with_current()
    placement = history[0]
    placement.end_placement(date(2026, 3, 1))
    assert placement.end_date == date(2026, 3, 1)
    assert not placement.is_current
    assert Placement.get_current(history) is None


# TC-5 (FR05, boundary): An end date on the start date is accepted.
def test_tc5_end_date_equal_to_start_date_is_accepted():
    history = make_history_with_current()
    history[0].end_placement(date(2026, 1, 15))
    assert history[0].end_date == date(2026, 1, 15)


# TC-6 (FR05, boundary): An end date one day before the start date is rejected.
def test_tc6_end_date_before_start_date_is_rejected():
    history = make_history_with_current()
    with pytest.raises(PlacementError, match="before the start date"):
        history[0].end_placement(date(2026, 1, 14))
    assert history[0].is_current


# TC-7 (FR05): A placement that is already closed cannot be ended again.
def test_tc7_closed_placement_cannot_be_ended_again():
    history = make_history_with_current()
    history[0].end_placement(date(2026, 3, 1))
    with pytest.raises(PlacementError, match="already closed"):
        history[0].end_placement(date(2026, 4, 1))
    assert history[0].end_date == date(2026, 3, 1)


# TC-8 (FR04, FR05, UC-3.2): Adding a new placement with an end date for the current one closes the old placement and makes the new one the current one.
def test_tc8_new_placement_closes_current_and_becomes_current():
    history = make_history_with_current()
    old = history[0]
    new = Placement.add_placement(
        history, 2, "Hope House", "Group home", date(2026, 3, 2), end_current_on=date(2026, 3, 1)
    )
    assert old.end_date == date(2026, 3, 1)
    assert new.is_current
    assert Placement.get_current(history) is new
    assert len(history) == 2


# TC-9 (NFR03): Adding a new placement without ending the current one is rejected, and nothing changes.
def test_tc9_new_placement_without_end_date_changes_nothing():
    history = make_history_with_current()
    with pytest.raises(PlacementError, match="Enter its end date first"):
        Placement.add_placement(history, 2, "Hope House", "Group home", date(2026, 3, 2))
    assert len(history) == 1
    assert history[0].is_current


# TC-10 (NFR03): If ending the current placement fails, it stays open and the new placement is not added.
def test_tc10_failed_end_keeps_current_open_and_new_not_added():
    history = make_history_with_current()
    with pytest.raises(PlacementError, match="before the start date"):
        Placement.add_placement(
            history, 2, "Hope House", "Group home", date(2026, 3, 2),
            end_current_on=date(2026, 1, 1),
        )
    assert len(history) == 1
    assert history[0].is_current
    assert history[0].end_date is None


# TC-11 (FR06): The history lists the current placement first, then past ones from newest to oldest.
def test_tc11_history_shows_current_first_then_newest_past():
    history = []
    Placement.add_placement(history, 1, "Rivera Family", "Foster family home (relative)", date(2025, 6, 1))
    Placement.add_placement(
        history, 2, "Hope House", "Group home", date(2025, 11, 1), end_current_on=date(2025, 10, 31)
    )
    Placement.add_placement(
        history, 3, "Lee Family", "Pre-adoptive home", date(2026, 2, 1), end_current_on=date(2026, 1, 31)
    )
    ordered = Placement.view_placement_history(history)
    assert [p.placement_id for p in ordered] == [3, 2, 1]
    assert ordered[0].is_current


# TC-12 (FR04): A placement with a blank name is rejected.
def test_tc12_blank_placement_name_is_rejected():
    history = []
    with pytest.raises(PlacementError, match="Placement name is required"):
        Placement.add_placement(history, 1, "   ", "Group home", date(2026, 1, 15))
    assert history == []


# TC-13 (FR05): Closing a placement with no end date is rejected.
def test_tc13_missing_end_date_is_rejected():
    history = make_history_with_current()
    with pytest.raises(PlacementError, match="End date is required"):
        history[0].end_placement(None)
    assert history[0].is_current


# TC-14 (FR04, FR05): The current placement cannot end after the new one starts, so two placements never overlap. Nothing changes.
def test_tc14_overlapping_placements_are_rejected():
    history = make_history_with_current()
    with pytest.raises(PlacementError, match="on or before the new start date"):
        Placement.add_placement(
            history, 2, "Hope House", "Group home", date(2026, 3, 2),
            end_current_on=date(2026, 3, 5),
        )
    assert len(history) == 1
    assert history[0].is_current
