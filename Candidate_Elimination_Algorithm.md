Initialize G to the set of most-general hypotheses in H
Initialize S to the set of most-specific hypotheses in H
For each training example, d, do:
    Remove from G hypotheses that do not match d
    For each hypothesis s in S that does not match d
      Remove s from S
      Add to S all minimal generalizations, h, of s such that:
        1) h matches d
        2) some member of G is more general or equal to h
      Remove from S any h that is more general than another hypothesis in S 
    If d is a negative example then:
      Remove form S hypotheses that match d 
      For each hypothesis g in G that matches d 
        Remove g from G 
        Add to G all minimal specializations, h, of g such that:
        1) h does not matches d
        2) some member of S is less general or equal to h
      Remove form G any h that is more specific than another hypothesis in G



