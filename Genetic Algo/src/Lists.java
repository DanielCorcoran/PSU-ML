public class Lists {
  public static final int POPULATION_SIZE = 10000;
  public static final int OBJ_LIST_SIZE = 1000;
  public static final int MUTATION_PCT = 50;

  /**
   * Creates a population of random genomes for the parents to be selected from
   * @param objectList
   *    List of the available objects from which the genome can be created
   * @return
   *    List of genomes that comprise the initial population
   */
  public GenomeNode[] createPopList(ObjectNode[] objectList) {
    GenomeNode[] population = new GenomeNode[POPULATION_SIZE];

    for (int i = 0; i < POPULATION_SIZE; i++){
      population[i] = createGenomeNode(objectList);
    }

    return population;
  }

  /**
   * Creates a list of objects of varying weights and values from 1-100 that will be used to create the genomes
   * @return
   *    List of objects used for the algorithm
   */
  public ObjectNode[] createObjectList(){
    ObjectNode[] objectList = new ObjectNode[OBJ_LIST_SIZE];

    for (int i = 0; i < OBJ_LIST_SIZE; i++) {
      objectList[i] = createObjectNode();
    }

    return objectList;
  }

  /**
   * @return
   *    Object with random weight and value
   */
  public ObjectNode createObjectNode(){
    int value = (int )(Math.random() * 100 + 1);
    int weight = (int )(Math.random() * 100 + 1);

    return new ObjectNode(value, weight);
  }

  /**
   * Creates a genome of randomly assigned objects
   * @param objectList
   *    List of objects from which the genome will be created
   * @return
   *    The new genome
   */
  public GenomeNode createGenomeNode(ObjectNode[] objectList){
    int[] genome = new int[OBJ_LIST_SIZE];

    for (int i = 0; i < genome.length; i++){
      if ((int )(Math.random() * 2) % 2 == 1)
        genome[i] = 1;
      else
        genome[i] = 0;
    }

    return new GenomeNode(genome, objectList);
  }

  /**
   * Flips the gene at a random index.  This occurs a number of times based on the percentage of genes that mutate
   * @param child
   *    Unmutated genome
   * @return
   *    Mutated genome
   */
  public int[] mutateChild(int[] child){
    if ((int )(Math.random() * 100 + 1) > MUTATION_PCT){
      int indexToMutate = (int )(Math.random() * Lists.OBJ_LIST_SIZE);
      if (child[indexToMutate] == 0)
        child[indexToMutate] = 1;
      else
        child[indexToMutate] = 0;
    }
    return child;
  }

  /**
   * Finds the genome with the lowest fitness index in the population.  This genome will be replaced with a new child
   * @param population
   *    List of genomes for consideration
   * @return
   *    Index of the genome with the lowest fitness index
   */
  public int findLowestFitnessIndex(GenomeNode[] population){
    int lowestFitness = OBJ_LIST_SIZE * 100;
    int lowestFitnessIndex = 0;

    for (int i = 0; i < population.length; i++){
      if (population[i].getFitness() < lowestFitness){
        lowestFitness = population[i].getFitness();
        lowestFitnessIndex = i;
      }
    }
    return lowestFitnessIndex;
  }

  /**
   * Finds the genome with the second lowest fitness index in the population.  This genome will be replaced
   * @param population
   *    List of genomes for consideration
   * @param lowestFitnessIndex
   *    Index of the genome with the lowest fitness index
   * @return
   *    Index of the genome with the second lowest fitness index
   */
  public int findSecondLowestFitnessIndex(GenomeNode[] population, int lowestFitnessIndex){
    int secondLowestFitness = OBJ_LIST_SIZE * 100;
    int secondLowestFitnessIndex = 0;

    for (int i = 0; i < population.length; i++){
      if (population[i].getFitness() < secondLowestFitness && i != lowestFitnessIndex){
        secondLowestFitness = population[i].getFitness();
        secondLowestFitnessIndex = i;
      }
    }
    return secondLowestFitnessIndex;
  }

  /**
   * Finds the index of the genome with the highest fitness index.  This is performed after all selection has taken
   * place, so is the most optimal genome in the population
   * @param population
   *    Population of genomes for consideration
   * @return
   *    Index of the genome with the highest fitness index
   */
  public int findHighestFitnessIndex(GenomeNode[] population){
    int highestFitness = 0;
    int highestFitnessIndex = 0;

    for (int i = 0; i < population.length; i++){
      if (population[i].getFitness() > highestFitness){
        highestFitness = population[i].getFitness();
        highestFitnessIndex = i;
      }
    }
    return highestFitnessIndex;
  }
}
