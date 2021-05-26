all_router = {}
check_neighbour = {}


class Router:
    def __init__(self, router):
        self.__router = router
        self.neighbour = []
        self.network = {}
        self.router_table = []

    def print_neighbour(self):
        if len(self.neighbour) == 0:
            return None
        else:
            return ", ".join(sorted(self.neighbour))

    def print_network(self):
        if len(self.network) == 0:
            return None
        else:
            for i in self.network:
                net_pairs = i + ":" + str(self.network[i])
                if net_pairs not in self.router_table:
                    self.router_table.append(net_pairs)
        return ", ".join(sorted(self.router_table))

    def print_info(self):
        print(" ", self.__router)
        if self.print_neighbour() == None:
            print("    N:")
        else:
            print("    N:", self.print_neighbour())
        if self.print_network() == None:
            print("    R:")
        else:
            print("    R:", self.print_network())

    def add_neighbour(self, neighbour):
        if len(self.neighbour) == 0:
            self.neighbour.append(neighbour.__router)
            check_neighbour[self.__router] = self.neighbour
        else:
            if neighbour.__router not in self.neighbour:
                self.neighbour.append(neighbour.__router)
                check_neighbour[self.__router] = self.neighbour

    def add_network(self, network, distance):
        if len(self.network) == 0:
            self.network[network] = distance
        else:
            for i in self.network.keys():
                if i != network:
                    self.network[network] = distance

    def receive_routing_table(self, neighbour):
        if len(self.network) == 0:
            for i in neighbour.network:
                new_distance = neighbour.network[i] + 1
                self.network[i] = new_distance
        else:
            for i in neighbour.network:
                if i not in self.network:
                    new_distance = neighbour.network[i] + 1
                    self.network[i] = new_distance

    def has_route(self, network):
        if network in self.network:
            if self.network[network] == 0:
                print("Router is an edge router for the network.")
                return
            else:
                print("Network {} is {} hops away".format(network, self.network[network]))
                return
        else:
            print("Route to the network is unknown.")
            return

def read_file(routerfile):

    while True:
        try:
            openfile = open(routerfile, "r")

            for row in openfile:
                name, neighbours, network = row.rstrip().split("!")
                router = Router(name)
                all_router[name] = router

                if neighbours != "":
                    for i in neighbours.split(";"):
                        naapuri = Router(i)
                        router.add_neighbour(naapuri)

                if network != "":
                    n, d = network.split(":")
                    router.add_network(str(n), int(d))

            openfile.close()
            return all_router

        except OSError:
            print("Error: the file could not be read or there is something wrong with it.")
            return False


def main():

    routerfile = input("Network file: ")

    if routerfile != "":
        read_routers = read_file(routerfile)

        if not read_routers:
            return

    while True:

        command = input("> ")
        command = command.upper()

        if command == "P":
            router = input("Enter router name: ")
            if router in all_router.keys():
                all_router[router].print_info()
            else:
                print("Router was not found.")

        elif command == "PA":
            for i in all_router.keys():
                all_router[i].print_info()
            pass

        elif command == "S":
            router = input("Sending router: ")
            for i in check_neighbour:
                if router in check_neighbour[i]:
                    all_router[i].receive_routing_table(all_router[router])

        elif command == "C":
            first_r = input("Enter 1st router: ")
            second_r = input("Enter 2nd router: ")
            all_router[first_r].add_neighbour(all_router[second_r])
            all_router[second_r].add_neighbour(all_router[first_r])

        elif command == "RR":
            router = input("Enter router name: ")
            network = str(input("Enter network name: "))
            all_router[router].has_route(network)

        elif command == "NR":
            name = input("Enter a new name: ")
            if name in all_router.keys():
                print("Name is taken.")
            else:
                all_router[name] = Router(name)

        elif command == "NN":
            router = input("Enter router name: ")
            network = str(input("Enter network: "))
            distance = int(input("Enter distance: "))
            all_router[router].add_network(network, distance)

        elif command == "Q":
            print("Simulator closes.")
            return

        else:
            print("Erroneous command!")
            print("Enter one of these commands:")
            print("NR (new router)")
            print("P (print)")
            print("C (connect)")
            print("NN (new network)")
            print("PA (print all)")
            print("S (send routing tables)")
            print("RR (route request)")
            print("Q (quit)")

main()
