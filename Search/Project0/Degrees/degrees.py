import csv
import sys
from tabulate import tabulate


from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


# ------------------------------------------------------------------------
# ---------------------- Load data from CSV files -------------------------
# ------------------------------------------------------------------------

def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

# ------------------------------------------------------------------------
# ---------------------- Get person_id for a person's name ----------------
# ------------------------------------------------------------------------

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]

# ------------------------------------------------------------------------    
# --------------------------- Shortest Path ------------------------------
# ------------------------------------------------------------------------
def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    print(f"--------------------------- Looking for path from {source} to {target} -------------------------")    
    
    num_explored = 0
    start = Node(state=source, parent=None, action=None)    
    frontier = StackFrontier()
    frontier.add(start)
    explored = set()        #? explored is set because cant have duplicates    

    table_data=[]
    headers=["Iteracion", "Current Node(id_name, id_movie)", "Parent", "Action", "Frontier", "Explored"]
    iteration = 0
    
    while True:
        if frontier.empty():
            with open("tabla_no_solution.txt", "w") as file:
                file.write(tabulate(table_data, headers=headers, tablefmt="grid"))
            
            return None
    
        #Removemos el nodo que actual del frontier y lo trabajamos

        current_node = frontier.remove()
        num_explored += 1
        iteration += 1

        #Registrar informacion de la iteracion

        current_state = current_node.state
        parent_state = current_node.parent.state if current_node.parent else None
        action = current_node.action

        frontier_states = [n.state for n in frontier.frontier]
        explored_states = list(explored)

        table_data.append([
            iteration,
            current_state,
            parent_state,
            action,
            frontier_states,
            explored_states
        ])

        #Detectamos si el state del nodo actual corresponde con el target buscado
        if current_node.state == target:
            actions = []
            people = []

            #Recorremos los nodos hacia atras guardando el recorrido y almacenando la informacion de cada nodo recorrido.
            while current_node.parent is not None:
                actions.append(current_node.action)
                people.append(current_node.state)
                current_node = current_node.parent
            actions.reverse()
            people.reverse()            

            solution = list(zip(actions, people))


            with open("tabla_solution.txt", "w") as file:
                file.write(tabulate(table_data, headers=headers, tablefmt="grid"))
            
            #! ----------- Aqui deberiamos retornar la solucion -------------
            
            return solution
        
        explored.add(current_node.state)

        #Como no encontramos el target buscado ahora procedemos a recurrir a los neighbors        
        neighbors = neighbors_for_person(current_node.state)

        for action, state in neighbors:
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=current_node, action=action)
                frontier.add(child)                                


    



# ------------------------------------------------------------------------
# -------------Helper function to get neighbors for a person -------------
# ------------------------------------------------------------------------
def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors
    


# ------------------------------------------------------------------------
# ------------------------------ MAIN ------------------------------------
# ------------------------------------------------------------------------
def main():
    #!------------------- Load data from files into memory -------------------
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")


    #!------------------- Prompt user for source and target -------------------
    #! Source: person_id for the person who the user wants to start from
    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    
    print(f"Source: {people[source]['name']}")

    #!------ Target: person_id for the person who the user wants to end at ---
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    #!------------------------- Find shortest path ---------------------------
    path = shortest_path(source, target)


    #!---------------------------- Output path -------------------------------
    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)                                                 #? Number of degrees of separation
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


if __name__ == "__main__":
    main()
