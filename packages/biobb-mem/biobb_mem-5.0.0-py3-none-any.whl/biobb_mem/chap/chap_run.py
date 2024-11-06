#!/usr/bin/env python3

"""Module containing the Cpptraj Density class and the command line interface."""
import argparse
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools.file_utils import launchlogger
import random
import os


class CHAP(BiobbObject):
    """
    | biobb_mem CHAP
    | Wrapper of the Channel Annotation Package (CHAP) for analyzing pore geometry, hydrophobicity, and hydration state in protein channels and other macromolecular structures.
    | CHAP finds pores in biological macromolecules like ion channels and determines the hydration state of these permeation pathways. It can operate on both individual structures and on molecular dynamics trajectories. For more information, see the `CHAP documentation <http://www.channotation.org/docs/input_parameters/>`_.

    Args:
        input_top_path (str): Path to the input  topology file. File type: input. `Sample file <https://github.com/bioexcel/biobb_mem/raw/master/biobb_mem/test/data/A01JD/A01JD.pdb>`_. Accepted formats: tpr (edam:format_2333), gro (edam:format_2033), g96 (edam:format_2033), pdb (edam:format_1476), brk (edam:format_2033), ent (edam:format_1476).
        input_traj_path (str) (Optional): Path to the GROMACS trajectory file. File type: input. `Sample file <https://github.com/bioexcel/biobb_mem/raw/master/biobb_mem/test/data/A01JD/A01JD.xtc>`_. Accepted formats: xtc (edam:format_3875), trr (edam:format_3910), cpt (edam:format_2333), gro (edam:format_2033), g96 (edam:format_2033), pdb (edam:format_1476), tng (edam:format_3876).
        input_index_path (str) (Optional): Path to the GROMACS index file. File type: input. `Sample file <https://github.com/bioexcel/biobb_mem/raw/master/biobb_mem/test/data/A01JD/A01JD.ndx>`_. Accepted formats: ndx (edam:format_2033).
        output_obj_path (str): Path to the output Wavefront Object file containing CHAP results. File type: output. `Sample file <https://github.com/bioexcel/biobb_mem/raw/master/biobb_mem/test/reference/chap/chap_output.obj>`_. Accepted formats: obj (edam:format_2330).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **b** (*float*) - (None) First frame (in picoseconds) to read from trajectory.
            * **e** (*float*) - (None) Last frame (in picoseconds) to read from trajectory.
            * **df** (*float*) - (None) Only use frame if t MOD dt == first time (in picoseconds).
            * **tu** (*str*) - ("ps") [fs|ps|ns|us|ms|s] Unit for time values.
            * **sel_pathway** (*str*) - (None) Reference group that defines the permeation pathway (usually 'Protein').
            * **sel_solvent** (*str*) - (None) Group of small particles to calculate density of (usually 'Water').
            * **out_filename** (*str*) - ("chap_output") Base file name for output files without file extension.
            * **out_num_points** (*int*) - (1000) Number of spatial sample points that are written to the JSON output file.
            * **out_extrap_dist** (*float*) - (0.0) Extrapolation distance beyond the pathway endpoints for both JSON and OBJ output.
            * **out_grid_dist** (*float*) - (0.15) Controls the sampling distance of vertices on the pathway surface which are subsequently interpolated to yield a smooth surface. Very small values may yield visual artifacts.
            * **out_vis_tweak** (*float*) - (0.1) Visual tweaking factor that controls the smoothness of the pathway surface in the OBJ output. Varies between -1 and 1 (exclusively), where larger values result in a smoother surface. Negative values may result in visualisation artifacts.
            * **out_detailed** (*bool*) - (False) If true, CHAP will write detailed per-frame information to a newline delimited JSON file including original probe positions and spline parameters. This is mostly useful for debugging.
            * **pf_method** (*str*) - ("inplane_optim") [inplane_optim|cylindrical] Path finding method. The default inplane_optim implements the algorithm used in the HOLE programme, where the position of a probe sphere is optimised in subsequent parallel planes so as to maximise its radius. The alternative cylindrical simply uses a cylindrical volume as permeation pathway.
            * **pf_vdwr_database** (*str*) - ("hole_simple") [hole_amberuni|hole_bondi|hole_hardcore|hole_simple|hole_xplor|user] Database of van-der-Waals radii to be used in pore finding.
            * **pf_vdwr_fallback** (*float*) - (None) Fallback van-der-Waals radius for atoms that are not listed in van-der-Waals radius database. Unless this is set to a positive value, an error will be thrown if a pathway-forming atom has no associated van-der-Waals radius in the database.
            * **pf_vdwr_json** (*str*) - (None) JSON file with user defined van-der-Waals radii. Will be ignored unless -pf-vdwr-database is set to 'user'.
            * **pf_align_method** (*str*) - ("ipp") [none|ipp] Method for aligning pathway coordinates across time steps.
            * **pf_probe_step** (*float*) - (0.1) Step length for probe movement.
            * **pf_max_free_dist** (*float*) - (1.0) Maximum radius of pore.
            * **pf_max_probe_steps** (*int*) - (10000) Maximum number of steps the probe is moved in either direction.
            * **pf_sel_ipp** (*str*) - (None) Selection of atoms whose COM will be used as initial probe position. If not set, the selection specified with 'sel-pathway' will be used.
            * **pf_init_probe_pos** (*list*) - (None) Initial position of probe in probe-based pore finding algorithms. If set explicitly, it will overwrite the COM-based initial position set with the ippSelflag.
            * **pf_chan_dir_vec** (*list*) - ([0.0, 0.0, 1.0]) Channel direction vector. Will be normalised to unit vector internally.
            * **pf_cutoff** (*float*) - (None) Cutoff for distance searches in path finding algorithm. A value of zero or less means no cutoff is applied. If unset, an appropriate cutoff is determined automatically.
            * **sa_seed** (*int*) - (None) Seed used in pseudo random number generation for simulated annealing. If not set explicitly, a random seed is used.
            * **sa_max_iter** (*int*) - (0) Number of cooling iterations in one simulated annealing run.
            * **sa_init_temp** (*float*) - (0.1) Simulated annealing initial temperature.
            * **sa_cooling_fac** (*float*) - (0.98) Simulated annealing cooling factor.
            * **sa_step** (*float*) - (0.001) Step length factor used in candidate generation.
            * **nm_max_iter** (*int*) - (100) Number of Nelder-Mead simplex iterations in path finding algorithm.
            * **nm_init_shift** (*float*) - (0.1) Distance of vertices in initial Nelder-Mead simplex.
            * **pm_pl_margin** (*float*) - (0.75) Margin for determining pathway lining residues. A residue is considered to be pathway lining if it is no further than the local path radius plus this margin from the pathway's centre line.
            * **pm_pf_sel** (*str*) - ("name CA") Distance of vertices in initial Nelder-Mead simplex.
            * **de_method** (*str*) - ("kernel") [histogram|kernel] Method used for estimating the probability density of the solvent particles along the permeation pathway.
            * **de_res** (*float*) - (0.01) Spatial resolution of the density estimator. In case of a histogram, this is the bin width, in case of a kernel density estimator, this is the spacing of the evaluation points.
            * **de_bandwidth** (*float*) - (-1.0) Bandwidth for the kernel density estimator. Ignored for other methods. If negative or zero, bandwidth will be determined automatically to minimise the asymptotic mean integrated squared error (AMISE).
            * **de_bw_scale** (*float*) - (1.0) Scaling factor for the band width. Useful to set a bandwidth relative to the AMISE-optimal value.
            * **de_eval_cutoff** (*float*) - (5.0) Evaluation range cutoff for kernel density estimator in multiples of bandwidth. Ignored for other methods. Ensures that the density falls off smoothly to zero outside the data range.
            * **hydrophob_database** (*str*) - ("wimley_white_1996") [hessa_2005|kyte_doolittle_1982|monera_1995|moon_2011|wimley_white_1996|zhu_2016|memprotmd|user] Database of hydrophobicity scale for pore forming residues.
            * **hydrophob_fallback** (*float*) - (None) Fallback hydrophobicity for residues in the pathway defining group. If unset, residues missing in the database will cause an error."
            * **hydrophob_json** (*str*) - (None) JSON file with user defined hydrophobicity scale. Will be ignored unless -hydrophobicity-database is set to 'user'.
            * **hydrophob_bandwidth** (*float*) - (0.35) Bandwidth for hydrophobicity kernel.
            * **binary_path** (*str*) - ("chap") Path to the CHAP executable binary.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_mem.chap.chap_run import chap_run
            prop = {
                'pf_method': 'inplane_optim',
                'sel_pathway': 1
            }
            chap(input_top_path='/path/to/myTopology.pdb',
                 input_traj_path='/path/to/myTrajectory.xtc',
                 input_index_path='/path/to/myIndex.ndx',
                 output_obj_path='/path/to/results.obj',
                 properties=prop)

    Info:
        * wrapped_software:
            * name: CHAP
            * version: 0.9.1
            * license: other
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """

    def __init__(self, input_top_path, output_obj_path,
                 input_traj_path=None, input_index_path=None,
                 properties=None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {"input_top_path": input_top_path,
                   "input_traj_path": input_traj_path,
                   "input_index_path": input_index_path},
            "out": {"output_obj_path": output_obj_path}
        }

        self.b = properties.get('b', None)
        self.e = properties.get('e', None)
        self.df = properties.get('df', None)
        self.tu = properties.get('tu', 'ps')
        self.sel_pathway = properties.get('sel_pathway', None)
        self.sel_solvent = properties.get('sel_solvent', None)
        self.out_filename = properties.get('out_filename', 'chap_output')
        self.out_num_points = properties.get('out_num_points', 1000)
        self.out_extrap_dist = properties.get('out_extrap_dist', 0.0)
        self.out_grid_dist = properties.get('out_grid_dist', 0.15)
        self.out_vis_tweak = properties.get('out_vis_tweak', 0.1)
        self.out_detailed = properties.get('out_detailed', False)
        self.pf_method = properties.get('pf_method', 'inplane_optim')
        self.pf_vdwr_database = properties.get('pf_vdwr_database', 'hole_simple')
        self.pf_vdwr_fallback = properties.get('pf_vdwr_fallback', None)
        self.pf_vdwr_json = properties.get('pf_vdwr_json', None)
        self.pf_align_method = properties.get('pf_align_method', 'ipp')
        self.pf_probe_step = properties.get('pf_probe_step', 0.1)
        self.pf_max_free_dist = properties.get('pf_max_free_dist', 1.0)
        self.pf_max_probe_steps = properties.get('pf_max_probe_steps', 10000)
        self.pf_sel_ipp = properties.get('pf_sel_ipp', None)
        self.pf_init_probe_pos = properties.get('pf_init_probe_pos', None)
        self.pf_chan_dir_vec = properties.get('pf_chan_dir_vec', [0, 0, 1])
        self.pf_cutoff = properties.get('pf_cutoff', None)
        self.sa_seed = properties.get('sa_seed', random.randint(-2**63, 2**63 - 1))
        self.sa_max_iter = properties.get('sa_max_iter', 0)
        self.sa_init_temp = properties.get('sa_init_temp', 0.1)
        self.sa_cooling_fac = properties.get('sa_cooling_fac', 0.98)
        self.sa_step = properties.get('sa_step', 0.001)
        self.nm_max_iter = properties.get('nm_max_iter', 100)
        self.nm_init_shift = properties.get('nm_init_shift', 0.1)
        self.pm_pl_margin = properties.get('pm_pl_margin', 0.75)
        self.pm_pf_sel = properties.get('pm_pf_sel', 'name CA')
        self.de_method = properties.get('de_method', 'kernel')
        self.de_res = properties.get('de_res', 0.01)
        self.de_bandwidth = properties.get('de_bandwidth', -1.0)
        self.de_bw_scale = properties.get('de_bw_scale', 1.0)
        self.de_eval_cutoff = properties.get('de_eval_cutoff', 5.0)
        self.hydrophob_database = properties.get('hydrophob_database', 'wimley_white_1996')
        self.hydrophob_fallback = properties.get('hydrophob_fallback', None)
        self.hydrophob_json = properties.get('hydrophob_json', None)
        self.hydrophob_bandwidth = properties.get('hydrophob_bandwidth', 0.35)
        self.binary_path = properties.get('binary_path', 'chap')
        self.properties = properties

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`CHAP <chap.chap_run.CHAP>` chap.chap_run.CHAP object."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # save current directory and move to temporary
        cwd = os.getcwd()
        os.chdir(self.stage_io_dict.get("unique_dir"))
        # create cmd and launch execution
        # TODO: use self.doc_properties_dict to add non default flags
        self.cmd = [self.binary_path,
                    '-s', self.stage_io_dict['in']['input_top_path'],
                    '-tu', self.tu,
                    '-out-filename', self.out_filename,
                    '-out-num-points', str(self.out_num_points),
                    '-out-extrap-dist', str(self.out_extrap_dist),
                    '-out-grid-dist', str(self.out_grid_dist),
                    '-out-vis-tweak', str(self.out_vis_tweak),
                    '-out-detailed', str(self.out_detailed).lower(),
                    '-pf-method', self.pf_method,
                    '-pf-align-method', self.pf_align_method,
                    '-pf-probe-step', str(self.pf_probe_step),
                    '-pf-max-free-dist', str(self.pf_max_free_dist),
                    '-pf-max-probe-steps', str(self.pf_max_probe_steps),
                    '-pf-chan-dir-vec', ' '.join(map(str, self.pf_chan_dir_vec)),
                    '-sa-seed', str(self.sa_seed),
                    '-sa-max-iter', str(self.sa_max_iter),
                    '-sa-init-temp', str(self.sa_init_temp),
                    '-sa-cooling-fac', str(self.sa_cooling_fac),
                    '-sa-step', str(self.sa_step),
                    '-nm-max-iter', str(self.nm_max_iter),
                    '-nm-init-shift', str(self.nm_init_shift),
                    '-pm-pl-margin', str(self.pm_pl_margin),
                    '-pm-pf-sel', f"'{self.pm_pf_sel}'",
                    '-de-method', self.de_method,
                    '-de-res', str(self.de_res),
                    '-de-bandwidth', str(self.de_bandwidth),
                    '-de-bw-scale', str(self.de_bw_scale),
                    '-de-eval-cutoff', str(self.de_eval_cutoff),
                    '-hydrophob-database', self.hydrophob_database,
                    '-hydrophob-bandwidth', str(self.hydrophob_bandwidth),
                    ]
        if self.stage_io_dict['in'].get('input_traj_path'):
            self.cmd.extend(['-f', self.stage_io_dict['in']['input_traj_path']])
        if self.stage_io_dict['in'].get('input_index_path'):
            self.cmd.extend(['-n', self.stage_io_dict['in']['input_index_path']])
        if self.b:
            self.cmd.extend(['-b', str(self.b)])
        if self.e:
            self.cmd.extend(['-e', str(self.e)])
        if self.df:
            self.cmd.extend(['-df', str(self.df)])
        if self.sel_pathway:
            self.cmd.extend(['-sel-pathway', str(self.sel_pathway)])
        if self.sel_solvent:
            self.cmd.extend(['-sel-solvent', str(self.sel_solvent)])
        if self.pf_vdwr_fallback:
            self.cmd.extend(['-pf-vdwr-fallback', self.pf_vdwr_fallback])
        if self.pf_vdwr_fallback == 'user':
            self.cmd.extend(['-pf-vdwr-database', self.pf_vdwr_fallback])
            if self.pf_vdwr_json:
                self.cmd.extend(['-pf-vdwr-json', self.pf_vdwr_json])
        if self.pf_sel_ipp:
            self.cmd.extend(['-pf-sel-ipp', self.pf_sel_ipp])
        if self.pf_init_probe_pos:
            self.cmd.extend(['-pf-init-probe-pos', ' '.join(map, str(self.pf_init_probe_pos))])
        if self.pf_cutoff:
            self.cmd.extend(['-pf-cutoff', str(self.pf_cutoff)])
        if self.hydrophob_fallback:
            self.cmd.extend(['-hydrophob-fallback', self.hydrophob_fallback])
        if self.hydrophob_database == 'user':
            self.cmd.extend(['-hydrophob-database', self.hydrophob_database])
            if self.hydrophob_json:
                self.cmd.extend(['-hydrophob-json', self.pf_vdwr_json])

        # Run Biobb block
        self.run_biobb()
        # move back to original directory
        os.chdir(cwd)
        # Copy files to host
        self.copy_to_host()
        # remove temporary folder(s)
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir"),
        ])
        self.remove_tmp_files()
        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def chap_run(input_top_path: str, output_obj_path: str,
             input_traj_path: str = None, input_index_path: str = None,
             properties: dict = None, **kwargs) -> int:
    """Execute the :class:`CHAP <chap.chap_run.CHAP>` class and
    execute the :meth:`launch() <chap.chap_run.CHAP.launch>` method."""

    return CHAP(input_top_path=input_top_path,
                input_traj_path=input_traj_path,
                input_index_path=input_index_path,
                output_obj_path=output_obj_path,
                properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Channel Annotation Package (CHAP) for analyzing pore geometry, hydrophobicity, and hydration state in protein channels and other macromolecular structures.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_top_path', required=True, help='Path to the input structure or topology file. Accepted formats: ent, gro, pdb, tpr.')
    parser.add_argument('--input_traj_path', required=False, help='Path to the input trajectory to be processed. Accepted formats: gro, pdb, tng, trr, xtc.')
    parser.add_argument('--input_index_path', required=False, help="Path to the GROMACS index file. Accepted formats: ndx.")
    required_args.add_argument('--output_obj_path', required=True, help='Path to the output processed Wavefront object. Accepted formats: obj.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call of each building block
    chap_run(input_top_path=args.input_top_path,
             input_traj_path=args.input_traj_path,
             input_index_path=args.input_index_path,
             output_obj_path=args.output_obj_path,
             properties=properties)


if __name__ == '__main__':
    main()
