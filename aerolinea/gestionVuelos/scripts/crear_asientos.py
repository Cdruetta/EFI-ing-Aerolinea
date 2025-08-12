from gestionVuelos.models import Seat

def crear_asientos_para_avion(plane):
    capacity = plane.capacity
    seat_columns = ["A", "B", "C", "D", "E", "F"]
    seat_types = {
        "A": "window",
        "F": "window",
        "B": "middle",
        "E": "middle",
        "C": "aisle",
        "D": "aisle",
    }
    num_rows = capacity // 6
    if capacity % 6 != 0:
        num_rows += 1

    for row in range(1, num_rows + 1):
        for col in seat_columns:
            seat_number = f"{row}{col}"
            seat_index = (row - 1) * 6 + seat_columns.index(col) + 1
            if seat_index > capacity:
                break

            Seat.objects.create(
                plane=plane,
                number=seat_number,
                row=row,
                column=col,
                seat_type=seat_types[col],
                status="available",
                extra_legroom=False,
                emergency_exit=False,
            )
