public class ObjectNode {
  private int value;
  private int weight;

  /**
   *
   * @param valueIn
   *    Value to give the object
   * @param weightIn
   *    Weight to give the object
   */
  public ObjectNode(int valueIn, int weightIn){
    this.value = valueIn;
    this.weight = weightIn;
  }

  /**
   *
   * @return
   *    Value of the object
   */
  public int getValue(){
    return this.value;
  }

  /**
   *
   * @return
   *    Weight of the object
   */
  public int getWeight(){
    return this.weight;
  }
}
