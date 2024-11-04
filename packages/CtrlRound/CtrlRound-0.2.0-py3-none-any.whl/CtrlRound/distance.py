#all distance functions must acces input parameters partial_solution, initial_values, constraints, constraint_values


def define_margin_distance(func, normalized=True):  
  #define the distance function used through the aggregation function used on the margins
  def calculate_margin_distance(partial_solution, initial_values, constraints, constraint_values):
      # merge the solution so far with initial values for the cells where no decision has been taken yet
      current_values = initial_values.copy()
      for cell,val in partial_solution.items():
          current_values[cell]=val
          
      nCell = len(partial_solution)        
      marginDiscrepancies = []
      for cons in constraints:
        target_value = constraint_values[cons]
        current_value = sum(current_values[cell_id] for cell_id in constraints[cons])
        marginDiscrepancies.append(abs(target_value - current_value)) 
      # marginDiscrepancies = [abs(constraint_values[cons] - sum(current_values[cell_id] for cell_id in constraints[cons])) for cons in constraints]
      if nCell >1 and normalized:
        return func(marginDiscrepancies)/nCell
      else:
        return func(marginDiscrepancies) 
  return calculate_margin_distance

def calculate_margin_distance(partial_solution, initial_values, constraints, constraint_values):
    # merge the solution so far with initial values for the cells where no decision has been taken yet
    current_values = initial_values.copy()
    for cell,val in partial_solution.items():
        current_values[cell]=val
        
    nCell = max(len(partial_solution),1)
    marginDiscrepancies = []
    for cons in constraints:
      target_value = constraint_values[cons]
      current_value = sum(current_values[cell_id] for cell_id in constraints[cons])
      marginDiscrepancies.append(abs(target_value - current_value)) 
    # marginDiscrepancies = [abs(constraint_values[cons] - sum(current_values[cell_id] for cell_id in constraints[cons])) for cons in constraints]
    return [max(marginDiscrepancies),sum(marginDiscrepancies)/nCell ]


def define_interior_distance(func, normalized=True): 
  #define a distance function on the interior cells
  def calculate_interior_distance(partial_solution, initial_values, constraints, constraint_values):
      # calculate the deviation from the origianl values in the interior cells
      # constraints and constraints values are not used but are input parameter to have a uniform interface across all distance functions
      if len(partial_solution) == 0 :
        return 0
      nCell = len(partial_solution) 
      if nCell >1 and normalized:
        return func(abs(partial_solution[cell] - initial_values[cell]) for cell in partial_solution)/nCell
      else:
        return func(abs(partial_solution[cell] - initial_values[cell]) for cell in partial_solution)
      
  return calculate_interior_distance

def define_total_distance(normalized=True): 
  calculate_margin_distance   = define_interior_distance(sum, normalized=normalized)
  calculate_interior_distance = define_margin_distance(sum, normalized=normalized)
  
  def calculate_total_distance(partial_solution, initial_values, constraints, constraint_values):
    return calculate_margin_distance(partial_solution, initial_values, constraints, constraint_values) + calculate_interior_distance(partial_solution, initial_values, constraints, constraint_values)
  
  return calculate_total_distance