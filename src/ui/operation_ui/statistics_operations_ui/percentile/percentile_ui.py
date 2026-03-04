        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="1">
                <tr>
                    <td valign="middle">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td>
                                    25th Percentile : {self.variable_1}
                                    <br>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    50h Percentile : {self.variable_2}
                                    <br>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    75th Percentile : {self.variable_3}
                                    <br>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
            """
        self.dynamic_formula.setText(html_formul)
