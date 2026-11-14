"""
Placement unit for the Foster Care Case Management System (Team 03).

This module is the business logic layer's Placement unit from the class
diagram in Section 2.5.2:

    Placement
      - placementID, placementName, placementType, startDate, endDate
      + addPlacement()
      + endPlacement()
      + viewPlacementHistory()

Requirements covered:
    FR04  Add a placement with a start date and placement details.
    FR05  Record an end date to close the current placement before a new one.
    FR06  View placement history, current placement first, then past ones.
    NFR03 A save happens completely or not at all. If ending the current
          placement fails, it stays open and the new placement is not added.
    NFR13 Every placement type maps to a federal AFCARS placement setting.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import List, Optional


# Placement settings allowed for a placement type (NFR12, NFR13).
# Based on the AFCARS "current placement setting" categories.
AFCARS_PLACEMENT_TYPES = frozenset({
    "Pre-adoptive home",
    "Foster family home (relative)",
    "Foster family home (non-relative)",
    "Group home",
    "Institution",
    "Supervised independent living",
    "Trial home visit",
})


class PlacementError(ValueError):
    """Raised when a placement request breaks a placement rule."""


@dataclass
class Placement:
    """One placement record for a child."""

    placement_id: int
    placement_name: str
    placement_type: str
    start_date: Optional[date]
    end_date: Optional[date] = None

    def __post_init__(self) -> None:
        # FR04: a placement needs a name, a valid type, and a start date.
        if not self.placement_name or not self.placement_name.strip():
            raise PlacementError("Placement name is required.")
        if self.placement_type not in AFCARS_PLACEMENT_TYPES:
            raise PlacementError(
                f"Placement type '{self.placement_type}' is not an AFCARS placement setting."
            )
        if self.start_date is None:
            raise PlacementError("Start date is required.")
        if self.end_date is not None and self.end_date < self.start_date:
            raise PlacementError("End date cannot be before the start date.")

    @property
    def is_current(self) -> bool:
        """A placement is current while it has no end date."""
        return self.end_date is None

    # endPlacement()

    def end_placement(self, end_date: Optional[date]) -> None:
        """Close this placement (FR05).

        The end date must be on or after the start date. A placement that is
        already closed cannot be ended again.
        """
        self._check_end_date(end_date)
        self.end_date = end_date

    def _check_end_date(self, end_date: Optional[date]) -> None:
        """Validate an end date without changing anything."""
        if not self.is_current:
            raise PlacementError("This placement is already closed.")
        if end_date is None:
            raise PlacementError("End date is required to close a placement.")
        if end_date < self.start_date:
            raise PlacementError("End date cannot be before the start date.")


    # addPlacement()

    @staticmethod
    def add_placement(
        history: List["Placement"],
        placement_id: int,
        placement_name: str,
        placement_type: str,
        start_date: Optional[date],
        end_current_on: Optional[date] = None,
    ) -> "Placement":
        """Add a new placement to a child's placement history (FR04).

        If the child already has a current placement, the caseworker must
        give an end date for it (UC-3.2 End Current Placement). Every check
        runs before anything changes, so the save is all or nothing (NFR03).
        """
        # Build the new placement first. This raises if any field is invalid.
        new_placement = Placement(placement_id, placement_name, placement_type, start_date)

        current = Placement.get_current(history)
        if current is not None:
            if end_current_on is None:
                raise PlacementError(
                    "The child has a current placement. Enter its end date first."
                )
            current._check_end_date(end_current_on)
            if end_current_on > new_placement.start_date:
                raise PlacementError(
                    "The current placement must end on or before the new start date."
                )

        # All checks passed. Apply both changes together.
        if current is not None:
            current.end_placement(end_current_on)
        history.append(new_placement)
        return new_placement


    # viewPlacementHistory()
  
    @staticmethod
    def view_placement_history(history: List["Placement"]) -> List["Placement"]:
        """Return the current placement first, then past ones, newest first (FR06)."""
        current = [p for p in history if p.is_current]
        past = sorted(
            (p for p in history if not p.is_current),
            key=lambda p: p.start_date,
            reverse=True,
        )
        return current + past

    @staticmethod
    def get_current(history: List["Placement"]) -> Optional["Placement"]:
        """Return the child's open placement, or None."""
        for placement in history:
            if placement.is_current:
                return placement
        return None
