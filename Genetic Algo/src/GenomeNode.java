public class GenomeNode {
  public static final int MAX_WEIGHT = 25000;
  private int[] genome = new int[Lists.OBJ_LIST_SIZE];
  private int fitness;

  /**
   * Creates a new genome.  If the total weight of the genome exceeds the max weight, the fitness becomes 0 (since the
   * genome cannot be used
   * @param genomeIn
   *    List of genes used to create the genome.  1 if the object is in the genome, 0 if not
   * @param objectsIn
   *    List of objects that correspond to the genes
   */
  public GenomeNode(int[] genomeIn, ObjectNode[] objectsIn){
    System.arraycopy(genomeIn, 0, this.genome, 0, this.genome.length);
    this.fitness = 0;

    int weight = 0;
    for (int i = 0; i < this.genome.length; i++){
      if (this.genome[i] == 1){
        this.fitness += objectsIn[i].getValue();
        weight += objectsIn[i].getWeight();
      }
    }

    if (weight > MAX_WEIGHT){
      this.fitness = 0;
    }
  }

  /**
   *
   * @return
   *    Returns the genome
   */
  public int[] getGenome(){
    return this.genome;
  }

  /**
   *
   * @return
   *    Fitness index of the genome
   */
  public int getFitness(){
    return this.fitness;
  }

  /**
   *
   * @param objectList
   *    List of objects used to calculate the weight of the genome
   * @return
   *    Weight of the genome
   */
  public int getWeight(ObjectNode[] objectList){
    int weight = 0;

    for (int i = 0; i < this.genome.length; i++){
      if (this.genome[i] == 1){
        weight += objectList[i].getWeight();
      }
    }
    return weight;
  }

  /**
   *
   * @param objectList
   *    List of objects used to calculate the value of the genome
   * @return
   *    Value of the genome
   */
  public int getValue(ObjectNode[] objectList){
    int value = 0;

    for (int i = 0; i < this.genome.length; i++){
      if (this.genome[i] == 1){
        value += objectList[i].getValue();
      }
    }
    return value;
  }
}
