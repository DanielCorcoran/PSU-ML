public class Main {
  public static final int NUM_ITERATIONS = 500000;

  /**
   * This program uses a genetic algorithm to solve the knapsack problem.  All of the parameters were tuned to make the
   * results interesting; the program was able to easily determine the optimal genome with a lower population or smaller
   * object list size
   */
  public static void main(String[] args) {
    Lists l = new Lists();
    ObjectNode[] objectList = l.createObjectList();
    GenomeNode[] population = l.createPopList(objectList);
    GenomeNode parent1;
    GenomeNode parent2;

    for (int i = 0; i < NUM_ITERATIONS; i++){
      /*
        The parents are 2 different randomly selected genomes from the population.  After gene crossover occurs, the
        genomes with the lowest fitness index are replaced are replaced by the children that were just produced and the
        process repeats, strengthening the fitness of the population and increasing the overall optimality of the
        genomes until the limit of iterations has been reached.
       */
      parent1 = population[(int )(Math.random() * Lists.POPULATION_SIZE)];
      parent2 = population[(int )(Math.random() * Lists.POPULATION_SIZE)];

      while(parent1 == parent2){
        parent2 = population[(int )(Math.random() * Lists.POPULATION_SIZE)];
      }

      int crossoverIndex = (int )(Math.random() * Lists.OBJ_LIST_SIZE);

      int[] child1 = new int[Lists.OBJ_LIST_SIZE];
      int[] child2 = new int[Lists.OBJ_LIST_SIZE];

      for (int j = 0; j < crossoverIndex; j++){
        child1[j] = parent1.getGenome()[j];
        child2[j] = parent2.getGenome()[j];
      }

      for (int j = crossoverIndex; j < Lists.OBJ_LIST_SIZE; j ++) {
        child1[j] = parent2.getGenome()[j];
        child2[j] = parent1.getGenome()[j];
      }

      /*
        A number of genes in the children are randomly mutated based on the mutation % parameter.  This allows for
        alterations in the genomes that otherwise may not occur.
       */
      child1 = l.mutateChild(child1);
      child2 = l.mutateChild(child2);

      int lowestFitnessIndex = l.findLowestFitnessIndex(population);
      int secondLowestFitnessIndex = l.findSecondLowestFitnessIndex(population, lowestFitnessIndex);

      GenomeNode childNode1 = new GenomeNode(child1, objectList);
      GenomeNode childNode2 = new GenomeNode(child2, objectList);

      population[lowestFitnessIndex] = childNode1;
      population[secondLowestFitnessIndex] = childNode2;
    }

    int bestMember = l.findHighestFitnessIndex(population);

    System.out.println("The weights and values of the objects used in the best remaining member:");
    for (int i = 0; i < objectList.length; i++){
      if (population[bestMember].getGenome()[i] == 1) {
        System.out.println("Object" + (i + 1) + ": weight " + objectList[i].getWeight() +
                ", value " + objectList[i].getValue());
      }
    }
    System.out.println();

    System.out.println("Index of best member: " + bestMember);
    System.out.println("Value of best member: " + population[bestMember].getValue(objectList));
    System.out.println("Weight of best member: " + population[bestMember].getWeight(objectList));
  }
}
