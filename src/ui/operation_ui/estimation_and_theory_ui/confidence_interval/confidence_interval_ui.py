        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" >
                <tr>
                    <td valign="middle" style="padding-right: 10px;">
                        {self.variable_1_display} &plusmn; 
                    </td>
                    
                    <td valign="middle" style="padding-right: 10px;">
                        {self.variable_4_display}<sup>*</sup>
                    </td>
                    
                    <td valign="middle">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td align="center" style="border-bottom: 2px solid currentColor; padding: 0 10px 4px 10px;">
                                    {self.variable_3_display}
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 4px 10px 5px 10px;">
                                    &radic;{self.variable_2_display}
                                </td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="padding-left: 20px;">
                        = {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)
