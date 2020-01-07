
import numpy as np

VERBOSE = True


class Converter:

    def __init__(self):
        # Dictionary of the masses of elements indexed by element name;
        # includes X for dummy atoms
        self.masses = {'X': 0, 'C': 12.011,'CA': 12.011, 'N': 14.00674, 'O': 15.9994,'S':32,'P':30.97 ,"F":18.998 }
        self.total_mass = 0
        self.cartesian = []
        self.zmatrix = []

        """
        The zmatrix is a list with each element formatted as follows
        [ name, [[ atom1, distance ], [ atom2, angle ], [ atom3, dihedral ]], mass , t]
        The first three atoms have blank lists for the undefined coordinates
        """


    def read_cartesian(self, input_file='cartesian.cart'):
        """
        Read the cartesian coordinates file (assumes no errors)
        The cartesian coordiantes consist of a list of atoms formatted as follows
        [ aa, name, np.array( [ x, y, z ] ), mass , num ]
        """
        self.cartesian = []
        with open(input_file, 'r') as f:
            for line in f.readlines():
                aa, name, x, y, z , num = line.split()
                self.cartesian.append(
                    [name,
                     np.array([x, y, z], dtype='f8'),
                     self.masses[name[0]],(aa,name,num)])

        return self.cartesian

#----------------------------------------------------------------------------------------------------------------

    def add_first_three_to_zmatrix(self):
        #unique trt 4 1st 3
        # First atom
        self.zmatrix = []
        name, position, mass,t = self.cartesian[0]
        self.zmatrix.append([name, [[0,0], [0,0], [0,0]], mass,t])

        # Second atom
        if len(self.cartesian) > 1:
            name, position, mass ,t = self.cartesian[1]
            atom1 = self.cartesian[0]
            pos1 = atom1[1]
            q = pos1 - position
            distance = np.sqrt(np.dot(q, q))
            self.zmatrix.append([name, [[0, distance], [0,0], [0,0]], mass,t])

        # Third atom
        if len(self.cartesian) > 2:
            name, position, mass,t = self.cartesian[2]
            atom1, atom2 = self.cartesian[:2]
            pos1, pos2 = atom1[1], atom2[1]
            q = pos1 - position
            r = pos2 - pos1
            q_u = q / np.sqrt(np.dot(q, q))
            r_u = r / np.sqrt(np.dot(r, r))
            distance = np.sqrt(np.dot(q, q))
            # Angle between a and b = acos(dot(a, b)) / (|a| |b|))
            angle = np.arccos(np.dot(-q_u, r_u))
            self.zmatrix.append(
                [name, [[0, distance], [1, np.degrees(angle)], [0,0]], mass,t])
#-------------------------------------------------------------------------------------------------------------------------------------------------

    def add_atom_to_zmatrix(self, i, line):
        """Generates an atom for the zmatrix
        (assumes that three previous atoms have been placed in the cartesian coordiantes)"""
        name, position, mass ,t = line
        atom1, atom2, atom3 = self.cartesian[:3]
        pos1, pos2, pos3 = atom1[1], atom2[1], atom3[1]
        # Create vectors pointing from one atom to the next
        q = pos1 - position
        r = pos2 - pos1
        s = pos3 - pos2
        position_u = position / np.sqrt(np.dot(position, position))
        # Create unit vectors
        q_u = q / np.sqrt(np.dot(q, q))
        r_u = r / np.sqrt(np.dot(r, r))
        s_u = s / np.sqrt(np.dot(s, s))
        distance = np.sqrt(np.dot(q, q))
        # Angle between a and b = acos(dot(a, b)) / (|a| |b|))
        angle = np.arccos(np.dot(-q_u, r_u))
        angle_123 = np.arccos(np.dot(-r_u, s_u))
        # Dihedral angle = acos(dot(normal_vec1, normal_vec2)) / (|normal_vec1| |normal_vec2|))
        plane1 = np.cross(q, r)
        plane2 = np.cross(r, s)
        dihedral = np.arccos(np.dot(
            plane1, plane2) / (np.sqrt(np.dot(plane1, plane1)) * np.sqrt(np.dot(plane2, plane2))))
        # Convert to signed dihedral angle
        if np.dot(np.cross(plane1, plane2), r_u) < 0:
            dihedral = -dihedral

        coords = [[0, distance], [1, np.degrees(angle)], [
            2, np.degrees(dihedral)]]
        atom = [name, coords, mass,t]
        self.zmatrix.append(atom)
#---------------------------------------------------------------------------------------
    def cartesian_to_zmatrix(self):
        """Convert the cartesian coordinates to a zmatrix"""
        self.add_first_three_to_zmatrix()
        for i, atom in enumerate(self.cartesian[3:], start=3):
            self.add_atom_to_zmatrix(i, atom)

        return self.zmatrix          
#-----------------------------------------------------------------------------------------------------------------------------------

    def output_zmatrix(self, output_file):
        """Output the zmatrix to the file"""
        with open(output_file, 'w') as f:
            f.write(self.str_zmatrix())

    def str_zmatrix(self):
        """Print the zmatrix"""
        out =""
        for atom, position, mass ,t in self.zmatrix:
            out += f'{atom:<1s}'
            for i in position:
                for j in range(0, len(i), 2):
                    out += f' {i[j] + 1:>4d} {i[j + 1]:>15.10f}'
            out+="\t" +t[0]+"\t"+t[1]+"\t"+t[2]
            out += '\n'

        return out.rstrip().replace("CA","c")
#------------------------------------------------------------------------------------------------------------------------------------


    def run_cartesian(self,input_file="c.cart",output_file="z.zm"):
        """Read in the cartesian coordinates, convert to cartesian, and output the file"""
        self.read_cartesian(input_file)
        self.cartesian_to_zmatrix()
        self.output_zmatrix(output_file)
