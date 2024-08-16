package ar.edu.itba.ss;

import ar.edu.itba.ss.models.CIM;
import ar.edu.itba.ss.models.Context;
import ar.edu.itba.ss.models.Particle;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;
import java.util.Set;

public class CIMTest {

    @Test
    public void normalCIMNoNeighborsTest() {
        Context context = new Context(
                1.0,
                0.5,
                1,
                List.of(
                        new Particle(0, 0, 0.1, 1),
                        new Particle(1, 1, 0.1, 1)),
                false);

        Map<Integer, Set<Integer>> neighbors = new CIM(context).compute();

        for (Map.Entry<Integer, Set<Integer>> entry : neighbors.entrySet()) {
            if (!entry.getValue().isEmpty()) {
                Assertions.fail("There shouldn't be any neighbors");
            }
        }
    }

    @Test
    public void periodicCIMNeighborsTest() {
        Context context = new Context(
                1.0,
                0.5,
                1,
                List.of(
                        new Particle(0, 0, 0.1, 1),
                        new Particle(1, 1, 0.1, 1)),
                true);

        Map<Integer, Set<Integer>> neighbors = new CIM(context).compute();

        for (Map.Entry<Integer, Set<Integer>> entry : neighbors.entrySet()) {
            if (entry.getValue().isEmpty()) {
                Assertions.fail("There shouldn't be any particles without neighbors");
            }
        }
    }

    @Test
    public void periodicCIMNeighborsTest2() {
        Context context = new Context(
                3.0,
                1,
                3,
                List.of(
                        new Particle(0.5, 0.5, 0.1, 1), // 0
                        new Particle(1.5, 0.5, 0.1, 1), // 1
                        new Particle(2.5, 0.5, 0.1, 1), // 2
                        new Particle(0.5, 1.5, 0.1, 1), // 3
                        new Particle(1.5, 1.5, 0.1, 1), // 4
                        new Particle(2.5, 1.5, 0.1, 1), // 5
                        new Particle(0.5, 2.5, 0.1, 1), // 6
                        new Particle(1.5, 2.5, 0.1, 1), // 7
                        new Particle(2.5, 2.5, 0.1, 1) // 8
//                        new Particle(3, 1.5, 0.1, 1),   // 9
//                        new Particle(3, 3, 0.1, 1),     // 10
//                        new Particle(1.5, 3, 0.1, 1)    // 11
                ),
                true);

        var answers = Map.of(
                // Manually calculated
                0, List.of(1, 3, 2, 6),
                1, List.of(0, 2, 4, 7),
                2, List.of(1, 5, 0, 8),
                3, List.of(0, 4, 6, 5),
                4, List.of(1, 3, 5, 7),
                5, List.of(2, 4, 8, 3),
                6, List.of(3, 7, 0, 8),
                7, List.of(4, 6, 8, 1),
                8, List.of(5, 7, 6, 2)
        );

        Map<Integer, Set<Integer>> neighbors = new CIM(context).compute();

        for (Map.Entry<Integer, Set<Integer>> entry : neighbors.entrySet()) {
            if (answers.containsKey(entry.getKey())) {
                Assertions.assertTrue(entry.getValue().containsAll(answers.get(entry.getKey())));
            }
        }
    }

}
