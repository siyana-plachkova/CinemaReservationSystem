from database import Database
from reservations import Reservations
from movies import Movies
from projections import Projections
from settings import HALL_ROWS


class ReservationsSystemInterface:

    def __init__(self):
        self.db = Database()
        self.movies = Movies(self.db)
        self.projections = Projections(self.db)
        self.reservations = Reservations(self.db)

    def start(self):
        self._help()
        while True:
            command = input("command: ")

            if command == "show_movies":
                self._show_movies()
            elif command.startswith("show_movie_projections"):
                splitted_command = command.split(" ")

                if len(splitted_command) < 2:
                    print("Movie id is required")
                else:
                    parameters = splitted_command[1:]
                    movie_id = parameters[0]
                    date = parameters[1] if len(parameters) == 2 else None

                    self._show_movie_projections(movie_id, date)
            elif command == "make_reservation":
                self._make_reservation()
            elif command.startswith("cancel_reservation"):
                splitted_command = command.split(" ")

                if len(splitted_command) < 2:
                    print("Insert username to cancel reservation.")
                else:
                    parameters = splitted_command[1:]
                    name = parameters[0]

                    self._cancel_reservation(name)
            elif command == "help":
                self._help()
            elif command == "exit":
                self._exit()
                break

    def _show_movies(self):
        print("Current movies:")
        for result in self.movies.get_movies():
            print("[%d] - %s (%.1f)" % result)

    def _show_movie_projections(self, movie_id, date=None):
        movie = self.movies.get_movie_by_id(movie_id)
        print("Projections for movie '%s':" % movie[0])

        for result in self.projections.get_movie_projections(movie_id, date):
            if date:
                print("[%d] - %s (%s)" % (result[0], result[3], result[1]))
            else:
                print("[%d] - %s %s (%s)" % (result[0], result[2], result[3], result[1]))

    def _make_reservation(self):
        username = input("Step 1 (User): Choose name> ")
        number_of_tickets = int(input("Step 1 (User): Choose number of tickets> "))

        self._show_movies()

        movie_id = input("Step 2 (Movie): Choose a movie> ")

        self._show_movie_projections(movie_id)

        projection_id = input("Step 3 (Projection): Choose a projection> ")

        hall = self.reservations.make_hall(projection_id)

        print("  " + (" ".join([str(i) for i in list(range(1, HALL_ROWS + 1))])))
        iterator = 1
        for row in hall:
            print(str(iterator) + " " + (" ".join(row)))
            iterator += 1

        reserved_seats = []
        iterator = 0
        while iterator < number_of_tickets:
            reserve_seat = input("Step 4 (Seats): Choose seat %d > " % (iterator + 1))
            seat = tuple([int(n) for n in reserve_seat[1:-1].split(',')])
            if seat > (10, 10):
                print("Lol... NO!")
            elif hall[seat[0] - 1][seat[1] - 1] == "X":
                print("This seat is already taken!")
            else:
                reserved_seats.append(seat)
                hall[seat[0] - 1][seat[1] - 1] = "X"
                iterator += 1

        print("This is your reservation:")
        movie = self.movies.get_movie_by_id(movie_id)
        print("Movie: %s (%.1f)" % movie)
        projection = self.projections.get_projection(projection_id)
        print("Date and Time: %s %s (%s)" % (projection[2], projection[3], projection[1]))
        print("Seats: %s" % (", ".join([str(reserved_seat) for reserved_seat in reserved_seats])))

        confirmed = False
        while not confirmed:
            confirmation = input("Step 5 (Type 'finalize' to confirm or type 'reject' to reject) > ")

            if confirmation == "finalize":
                for seat in reserved_seats:
                    self.reservations.add_reservation(username, projection_id, seat[0], seat[1])
                confirmed = True

            if confirmation == "reject":
                print("This reservation was rejected.")
                return

    def _cancel_reservation(self, name):
        user_reservations = self.reservations.get_reservations(name)

        if not len(user_reservations):
            print("No resrvations for this user.")
        else:
            for row in user_reservations:
                print("[%d] - projection: %d, (%d, %d)" % row)

            projection_id = input("choose reservation for which projection to cancel > ")
            self.reservations.delete_reservation(name, projection_id)

            print("Reservation canceled!")

    def _help(self):
        help = ["Here is the list of commands (spells):",
                "   show_movies - Shows all movies ordered by rating",
                "   show_movie_projections <movie_id> [<date>] - Shows all movies projections with given movie id and date",
                "   make_reservation - Opens make reservation interface",
                "   cancel_reservation <name> - Cancels a reservation",
                "   exit - Exit the interface",
                "   help - This thing"]

        print("\n".join(help))

    def _exit(self):
        print("Exiting...")

if __name__ == '__main__':
    reservation_sys = ReservationsSystemInterface()
    reservation_sys.start()
